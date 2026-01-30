# 🚀 FMCG Pre-Implementation Migration Plan
**Option C - Hybrydowa (4 dni)**  
**Start:** 28 października 2025  
**Status:** 🟢 IN PROGRESS

---

## 📅 TIMELINE

### **DZIEŃ 1-2: Migracja Consulting → SQL** 🔴 CRITICAL
**Data:** 28-29 października 2025  
**Status:** 🔵 STARTED

#### Krok 1.1: Dry-run Migration (Max jako test)
- [ ] Uruchom migration script z --dry-run
- [ ] Zwaliduj dane (struktura, typy, relacje)
- [ ] Sprawdź czy wszystkie pola są mapowane
- [ ] Log issues (jeśli są)

#### Krok 1.2: Test Migration (Max)
- [ ] Backup users_data.json
- [ ] Uruchom migration dla Max
- [ ] Weryfikacja w SQL (test_sql_read.py)
- [ ] Test aplikacji (czy wszystko działa)
- [ ] Rollback test (restore z backupu)

#### Krok 1.3: Batch Migration (wszyscy użytkownicy)
- [ ] Faza 1: Migracja 5 użytkowników (test group)
- [ ] Validation + QA
- [ ] Faza 2: Migracja 15 użytkowników
- [ ] Validation + QA
- [ ] Faza 3: Migracja pozostałych
- [ ] Final validation

#### Krok 1.4: Switch Backend
- [ ] Update BaseRepository default backend: "json" → "sql"
- [ ] Test wszystkich funkcji
- [ ] Monitor performance
- [ ] Backup JSON (archive)

**Deliverable:** ✅ Consulting w SQL, jeden backend

---

### **DZIEŃ 3: Refactoring Data + API** 🟠 HIGH
**Data:** 30 października 2025  
**Status:** ⏳ PENDING

#### Krok 2.1: Cleanup Money/Coins
- [ ] Find all `bg_data["money"]` references
- [ ] Replace z `user_data["degencoins"]`
- [ ] Find all `bg_data["firm"]["coins"]`
- [ ] Remove deprecated fields
- [ ] Update utils/business_game.py functions
- [ ] Update views/business_games.py
- [ ] Test transactions (rewards, costs)

#### Krok 2.2: Standaryzacja API
- [ ] Find all direct JSON access: `grep -r "users_data.json"`
- [ ] Replace z UserRepository calls
- [ ] Update utils/achievements.py
- [ ] Update views/business_games.py (rankings)
- [ ] Test wszystkich endpointów

**Deliverable:** ✅ Jeden system monet + Repository API wszędzie

---

### **DZIEŃ 4: Testy + Cleanup** 🟡 MEDIUM
**Data:** 31 października 2025  
**Status:** ⏳ PENDING

#### Krok 3.1: Integration Tests
- [ ] Test Business Games flow (start → contracts → complete)
- [ ] Test Events system
- [ ] Test Employees (hire/fire)
- [ ] Test Office upgrades
- [ ] Test Rankings
- [ ] Test Historia tab

#### Krok 3.2: Performance Testing
- [ ] Monitor query times
- [ ] Check concurrent access
- [ ] SQL query optimization (jeśli potrzeba)

#### Krok 3.3: Cleanup Deprecated
- [ ] Remove backward compatibility code
- [ ] Remove old `business_game` singular references
- [ ] Update documentation
- [ ] Archive old migration scripts

**Deliverable:** ✅ Clean, tested, production-ready codebase

---

## **DZIEŃ 5+: FMCG Implementation Start** 🎯
**Data:** 1 listopada 2025+  
**Status:** ⏳ READY TO START

---

## 📊 CURRENT STATUS (Dzień 1 - 28.10.2025)

### ✅ COMPLETED
- [x] SQL infrastructure ready (models, connections)
- [x] UserRepository w SQL (users migrowani)
- [x] BusinessGameRepository gotowy (hybrydowy)
- [x] Migration scripts gotowe

### 🔵 IN PROGRESS
- [ ] Krok 1.1: Dry-run Migration (Max)

### ⏳ PENDING
- [ ] Krok 1.2-1.4: Full migration
- [ ] Dzień 3: Refactoring
- [ ] Dzień 4: Tests + Cleanup
- [ ] Dzień 5+: FMCG Start

---

## 🎯 SUCCESS CRITERIA

### Po Dniu 2 (Migration Complete):
- ✅ 100% użytkowników w SQL
- ✅ Backend = "sql" (default)
- ✅ Zero JSON file locks
- ✅ SQL queries działają (rankings, stats)

### Po Dniu 3 (Refactoring):
- ✅ Jedno źródło prawdy dla monet (degencoins)
- ✅ Wszystko przez Repository API
- ✅ Zero bezpośredniego JSON access

### Po Dniu 4 (Tests):
- ✅ All tests pass
- ✅ Performance OK (queries <100ms)
- ✅ Clean codebase (no deprecated)

### Dzień 5 (Ready):
- ✅ FMCG może startować w SQL
- ✅ Solidne fundamenty
- ✅ Skalowalne rozwiązanie

---

## 🚨 RISK MITIGATION

### Risk 1: Data Loss podczas migracji
**Mitigation:**
- ✅ Full backup przed każdą fazą
- ✅ Dry-run validation
- ✅ Phased migration (5 → 15 → all)
- ✅ Fast rollback (<5 min)

### Risk 2: Downtime podczas migration
**Mitigation:**
- ✅ Migration poza peak hours (3-6 AM)
- ✅ Może działać w tle (hybrydowy system)
- ✅ No breaking changes for users

### Risk 3: Hidden JSON dependencies
**Mitigation:**
- ✅ Grep all references przed zmianą
- ✅ Integration tests catch issues
- ✅ Gradual rollout

---

## 📞 CHECKPOINTS

### Checkpoint 1: Po Dry-run (Dzień 1)
**Pytanie:** Czy dane się zgadzają? Issues?  
**Decyzja:** GO/NO-GO dla full migration

### Checkpoint 2: Po Test Migration (Dzień 1)
**Pytanie:** Czy Max działa poprawnie w SQL?  
**Decyzja:** GO/NO-GO dla batch

### Checkpoint 3: Po Batch Migration (Dzień 2)
**Pytanie:** Wszyscy użytkownicy OK?  
**Decyzja:** Switch backend to SQL

### Checkpoint 4: Po Refactoring (Dzień 3)
**Pytanie:** API jednolite? Monety działają?  
**Decyzja:** Ready for tests

### Checkpoint 5: Po Tests (Dzień 4)
**Pytanie:** Production ready?  
**Decyzja:** GO for FMCG

---

## 📝 NEXT ACTIONS

### Teraz (Dzień 1 - 28.10):
1. **Backup users_data.json**
2. **Run dry-run migration dla Max**
3. **Validate results**
4. **Review issues (jeśli są)**

### Jutro (Dzień 2 - 29.10):
1. **Batch migration (phased)**
2. **Switch backend**
3. **Smoke tests**

### 30.10 (Dzień 3):
1. **Refactoring start**

---

**LET'S GO! 🚀**

Status będzie updateowany w tym pliku po każdym kroku.
