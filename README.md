# Introduction
WoW Tools

## Macro
### AutoFollow
/script if not UnitAffectingCombat("player") then if not UnitCanAttack("player","target") or UnitIsDead("target") then FollowUnit("爆裂莲雾") end end  

### LockTarget
/target player  
/target targettarget

### Attack
/castsequence [combat]spell_1,spell_2, ...
