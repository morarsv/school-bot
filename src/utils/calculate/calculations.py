def get_coins_per_lvl(h_lvl: int,
                      s_lvl: int) -> int:
    return h_lvl * 3 + (s_lvl*5) + 13


def get_cost_upgrade_school(s_lvl: int) -> int:
    if s_lvl >= 3:
        return 99999
    cost = {
        1: 50,
        2: 150,
        3: 300
    }
    return cost[s_lvl+1]


def calculate_accrual(xp: int, s_lvl: int) -> tuple[int, int]:
    xp += 20
    xp = 1099 if xp >= 1099 else xp
    h_lvl = xp // 100
    coins = get_coins_per_lvl(h_lvl=h_lvl, s_lvl=s_lvl)
    return xp, coins
