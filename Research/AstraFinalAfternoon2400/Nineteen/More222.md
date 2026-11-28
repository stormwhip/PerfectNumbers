# Canonical `(19,222)`: three more complete second fibers

Fixed baseline `495c59f55456a70994ce7848487e0c4e262c1984`. Interpret all exponents as exact in `N≤10^2400` odd perfect: first root `19^222`, then `t=7579985624053` with exponent `f`, then `r=3705121363` with exponent `g`. This packet excludes all three secondary prefixes `(f,g)=(1,40),(18,42),(18,46)`. These windows were unresolved and unrefined in the frozen tertiary packet; they are disjoint from the separately completed `f=2` first and `(f,g)=(1,2)`.

* **`(1,40)`**: `t¹` fixes Euler and forces prime `q=(t+1)/2=3789992812027`. The checker rebuilds all 21 exact live `q` exponents `2,4,…,42` and the strict raw tail **86**. Every one has two agreeing strict integer forest terminals; minimum diagnostic floor 2401.
* **`(18,42)` and `(18,46)`**: direct strict forest proofs on the entire exact prefix. All permissible Euler locations, including outside the forest, remain in the minimization. Both independent integer recurrences give strict bounds, diagnostic floors 2405 and 2400 respectively. Floor 2400 is only an output shorthand; exact integer comparison is strictly above `10^2400`.

The [checker](VerifyMore222.py) re-enumerates the original exact first, second and relevant third domains; it binds the exact prefixes to previously unresolved frozen branches and verifies every compulsory root, activated edge and prime witness. All 203 ECPP records in the [sealed packet](More222.json.gz) are used. SHA-256 `75e22e331489a04cf1ddd17f52c471bfddad3b684bb64f3d7493a071eaf224dd`. Isolated author replay exited 0, with 23 strict forests proving three complete second fibers.

```text
python -I -S -B -X int_max_str_digits=0 Research/AstraFinalAfternoon2400/Nineteen/VerifyMore222.py
```

After the earlier [first-fiber completion](First222F2.md) and [secondary completion](Root222F1G2.md), first `f=1` retains only second `{4,16,22,42,46}`, and first `f=18` retains only `{2,12,16,22}`. No complete first, exact key or shard is closed by this packet. No withdrawn PR #11 argument is used.
