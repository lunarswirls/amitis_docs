#!/usr/bin/env python
# -*- coding: utf-8 -
# Imports:
import argparse
import os
import mysql.connector
import re
from pathlib import Path
import sys
import json

# --------------------------------------------------
# SQL table definitions
# --------------------------------------------------
input_table = "amitis_input"
interior_table = "amitis_interior"


def parse_input_variables(filename: Path):
    """
    Parse a text file for lines like: variable = value
    - Strip anything after a '#'
    - Ignore lines that become empty or start with '#'
    - Return list of (variable, value) tuples.
    """
    pattern = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*(.+?)\s*$")
    variables = []

    with open(filename, 'r') as f:
        for line in f:
            # Remove trailing comments
            stripped = line.split('#', 1)[0].strip()

            # Skip empty or comment-only lines
            if not stripped:
                continue

            match = pattern.match(stripped)
            if match:
                var, val = match.groups()
                variables.append((var, val))
                # print(var, val)

    return variables


def parse_interior_variables(filename: Path):
    """
    Parse a text file for lines like:   0.0   0.0   0.0   2440.0e3   2440.0e3   2440.0e3   1.0e6
    - Return list of (variable, value) tuples.
    """
    rows = []

    with open(filename, 'r') as f:
        for line in f:
            values = line.split()
            if len(values) != 7:
                raise ValueError(
                    f"ITR file row does not contain 7 columns:\n{line}"
                )

            rows.append(values)

    return rows


def ensure_table_exists(cursor, table_name, columns):
    """
    Ensure a table exists with at least the given columns.
    Columns is a list of strings.
    """

    # Create table if it doesn't exist — minimal starting point
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            subdir TEXT,
            source_file TEXT
        )
    """)

    # Check existing columns via INFORMATION_SCHEMA
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = %s
    """, (table_name,))
    existing_cols = {row[0] for row in cursor.fetchall()}

    # Add missing columns (must specify type)
    for col in columns:
        if col not in existing_cols:
            cursor.execute(
                f"ALTER TABLE `{table_name}` ADD COLUMN `{col}` TEXT"
            )


def insert_input_variables(cursor, table_name, variables, subdir, source_file):
    """
    Insert a single row for the input file.
    `variables` is a list of (var, val) pairs.
    """

    # Extract variable names and ensure needed table columns
    variable_names = [var for var, _ in variables]
    ensure_table_exists(cursor, table_name, variable_names + ["subdir", "source_file"])

    # Check if entry exists
    cursor.execute(f"""
            SELECT 1 FROM `{table_name}`
            WHERE subdir = %s AND source_file = %s
            LIMIT 1
        """, (subdir, source_file))

    exists = cursor.fetchone()

    if exists:
        print("Entry already exists, skipping insert.")
        return False

    # Build dictionary of column → value
    row_data = {var: val for var, val in variables}
    row_data["subdir"] = subdir
    row_data["source_file"] = source_file

    # Prepare INSERT statement dynamically
    columns = ", ".join(f"`{c}`" for c in row_data.keys())
    placeholders = ", ".join(["%s"] * len(row_data))
    values = list(row_data.values())

    cursor.execute(
        f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})",
        values
    )
    return True


def ensure_itr_table(cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS `{interior_table}` (
            X          VARCHAR(255),
            Y          VARCHAR(255),
            Z          VARCHAR(255),
            R_x        VARCHAR(255),
            R_y        VARCHAR(255),
            R_z        VARCHAR(255),
            eta        VARCHAR(255),
            subdir     VARCHAR(255),
            source_file VARCHAR(255)
        )
    """)


def insert_itr_rows(cursor, table_name, rows, subdir, source_file):

    ensure_itr_table(cursor)

    # Check if entry exists
    cursor.execute(f"""
            SELECT 1 FROM `{table_name}`
            WHERE subdir = %s AND source_file = %s
            LIMIT 1
        """, (subdir, source_file))

    exists = cursor.fetchone()

    if exists:
        print("Entry already exists, skipping insert.")
        return False

    for row in rows:
        cursor.execute(f"""
            INSERT INTO `{table_name}`
            (X, Y, Z, R_x, R_y, R_z, eta, subdir, source_file)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, row + [subdir, source_file])

    return True


def main():
    parser = argparse.ArgumentParser(description="Database management tool for Amitis input files")
    parser.add_argument('amitis_db', help='JSON credentials for local Amitis MySQL database')
    parser.add_argument('--input_file', default=None, help='Amitis input file (*.inp)')
    parser.add_argument('--interior_file', default=None, help='Amitis interior file (*.itr)')
    parser.add_argument('--input_dir', default=None, help='Amitis input directory containing input file (*.inp) and interior file (*.itr)')
    args = parser.parse_args()

    if args.input_dir and not args.input_file and not args.interior_file:
        # if only input directory provided, fetch *.inp and *.itr files
        input_dir = Path(args.input_dir)

        # check job ran successfully
        err_files = list(input_dir.glob("*.err"))
        if len(err_files) == 1:
            err_file = err_files[0]

            if os.path.getsize(err_file) > 0:
                print("ERROR: Simulation did not run successfully, see log file for details.")
                sys.exit(1)
                # TODO: gracefully continue if searching directory recursively
        elif len(err_files) > 1:
            print("WARNING: More than one error file found, taking most recent file.")
            err_file = max(err_files, key=os.path.getmtime)

            if os.path.getsize(err_file) > 0:
                print("ERROR: Simulation did not run successfully, see log file for details.")
                sys.exit(1)
                # TODO: gracefully continue if searching directory recursively
        else:
            print("WARNING: No error file found, TODO add flag if test has been run yet.")
            # TODO: add flag if test has been run yet

        inp_files = list(input_dir.glob("*.inp"))
        itr_files = list(input_dir.glob("*.itr"))

        if not inp_files or not itr_files:
            print("ERROR: Directory must contain .inp and .itr files.")
            sys.exit(1)
        if len(inp_files) > 1:
            print("ERROR: More than one input file found, specify using --input_file argument.")
            sys.exit(1)
        if len(itr_files) > 1:
            print("ERROR: More than one interior file found, specify using --interior_file argument.")
            sys.exit(1)

        inp_file = inp_files[0]
        itr_file = itr_files[0]

    elif not args.input_dir and args.input_file and args.interior_file:
        # if input file and interior file provided and not input directory, validate file paths
        if os.path.isfile(args.input_file) and os.path.isfile(args.interior_file):
            inp_file = args.input_file
            itr_file = args.interior_file
        else:
            print("ERROR: Check that input and interior files exist.")
            sys.exit(1)

    elif args.input_dir and args.input_file and args.interior_file:
        # if both input directory and input and interior files provided, warn user and proceed with files
        print("WARNING: Taking file arguments and ignoring input_dir.")
        inp_file = os.path.isfile(args.input_file)
        itr_file = os.path.isfile(args.interior_file)
    else:
        print("ERROR: Either input directory or both Amitis input and interior files must be specified.")
        sys.exit(1)

    # Validate same directory
    if inp_file.parent != itr_file.parent:
        print("ERROR: .inp and .itr files must be in the same directory.")
        sys.exit(1)

    # Extract subdirectory name
    subdir_name = inp_file.parent.name

    # Parse variables, for now does not enforce any naming convention checks
    vars1 = parse_input_variables(inp_file)
    vars2 = parse_interior_variables(itr_file)

    # Open db connection and initialize cursor
    with open(args.amitis_db) as f:
        creds = json.load(f)

    conn = mysql.connector.connect(
        host=creds["host"],
        user=creds["user"],
        password=creds["password"],
        database=creds["database"],
        port=creds.get("port", 3306)
    )
    cur = conn.cursor()

    # Dump input and interior files to respective tables in db
    inp_success = insert_input_variables(cur, input_table, vars1, subdir_name, inp_file.name)
    itr_success = insert_itr_rows(cur, interior_table, vars2, subdir_name, itr_file.name)

    conn.commit()
    conn.close()

    if inp_success:
        print(f"Imported {len(vars1)} variables from {inp_file.name}")
    if itr_success:
        print(f"Imported {len(vars2)} conductivity profile(s) from {itr_file.name}")


if __name__ == "__main__":
    main()

