# Common Amitis errors

<details markdown="1">
<summary><b>(d_calc_charge_de:2244) |  CUDA error code: 700 | Reason: an illegal memory access was encountered</b></summary>

**Cause:** Large timestep → particles escape → array OOB.
**Fix:** Decrease `dt` or increase subcycles. [Read more here](./Amitis_Definitions.md#temporal-decomposition)
</details>

<details markdown="1">
<summary><b> Dummy error</summary>

**Cause:** Here write the cause  
**Fix:** Here write the fix
</details>