def cli_user_confirm_action(prompt: str) -> bool:
  print("")
  user_input = input(prompt + " ").lower().strip()
  
  if (user_input == 'y'):
    return True
  elif (user_input == 'n'):
    return False
  
  print("Invalid input!")
  cli_user_confirm_action(prompt)