from exif import Image

my_image = Image('/Users/swhite/pictures-from-old-backup-drive/Pictures/Photo Booth/Photo 47.jpg')
attributes = my_image.get_all
for item in attributes.items:
    print(item)