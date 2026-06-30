# class Dad:
#     def __init__(self):
#         print("爸爸建好房子：有墙、有门、有窗户")

# class Son(Dad):
#     def __init__(self):
#         super().__init__()  # 让爸爸先干活
#         print("我：搬进家具，住进去")

# son = Son()

class Dad:
    print("爸爸建好房子：有墙、有门、有窗户")

class Son(Dad):
    def __init__(self):
        super().__init__()  # 让爸爸先干活
        print("我：搬进家具，住进去")

son = Son()