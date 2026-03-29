def wait_and_get_return_from_user(reply_text):
    print("\n📩 Suggested Replies:\n")

    # Pretty display
    options = reply_text.split("Option ")[1:]

    for i, opt in enumerate(options, 1):
        print(f"\n🔹 Option {i}")
        print("-" * 30)
        print(opt.strip())

    # User input
    while True:
        choice = input("\n👉 Select option (1 / 2 / 3): ").strip()

        if choice in ["1", "2", "3"]:
            break
        else:
            print("❌ Invalid choice. Try again.")

    selected = extract_option(reply_text, int(choice))

    print("\n✅ Selected Reply:\n")
    print(selected)

    return selected


def extract_option(reply_text, option_number):
    options = reply_text.split("Option ")

    for opt in options:
        if opt.strip().startswith(str(option_number)):
            return "Option " + opt.strip()

    return "❌ Option not found"