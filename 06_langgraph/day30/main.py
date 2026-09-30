from long_term import save_user_preferences, get_user_preferences

save_user_preferences("user_1", {"theme": "dark", "language": "en"})

result = get_user_preferences("user_1")

print(result)
