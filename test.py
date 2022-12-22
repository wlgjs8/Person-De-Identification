import os

root = 'C:/Users/JeeheonKim/id_photo2/id_photo/Test Images/Aspect 3.jpg'
split_path = root.split('/')

# print(root)
# print(split_path)
# print(os.path.join(split_path[:-1]))

save_dir = 'C:\\.cache/'

print(save_dir)
print(os.path.abspath(save_dir))