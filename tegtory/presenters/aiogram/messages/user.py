from tegtory.domain.entities import User


def format_user(user: User) -> str:
    return f"""\
🌟 *Паспорт {user.name}*

💲 *Баланс:* {user.money:,}
⚔️ *SC:* {user.stolar:,}

🏆 *Рейтинг:* {user.rating:,}
🛡️ *Лига:* {user.league}

№ {user.id * (len(user.username) ** 2) // 2}
"""
