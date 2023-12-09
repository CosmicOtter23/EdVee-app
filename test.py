array = [3, 4, 5, 6]
keywords = ["append", "pop"]

for i in range(2):
  print(array)
  exec(f"array.{keywords[i]}(2)")
  print(array)