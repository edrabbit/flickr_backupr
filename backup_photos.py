import flickr_api
import codecs
import os
import subprocess

# TODO: Figure out how to download videos. Sometimes it downloads as a jpg? sometimes it fails?
# Ex: edrabbit, Stupid brush turkey, Video Original, http://www.flickr.com/photos/77866964@N00/8253619402
# IOError: [Errno 2] No such file or directory: u'saved/edrabbit/Stupid brush turkey 8253619402.com/photos/edrabbit/8253619402/play/orig/dfcb78ef55/'
# Ex: mooflyfoof, Tahoe Cabin - Morning, Original, http://www.flickr.com/photos/49128806@N00/8522733154
# Saved to saved/mooflyfoof/Tahoe Cabin - Morning 8522733154.jpg

SAVE_PATH = "saved2"

def save_exif(photo, saved_to_file):
    ''' Fetch the exif data and write it to the photo file
        photo: PhotoObject
        saved_to_file: the filename (without .jpg extension) of the saved photo
    '''
    # Write exif
    # TODO: We need to try/catch and delete image file if this fails
    try:
        tags = photo.getExif()
        # TODO: Should we save this to a file in case we miss something in xml writing?
    except flickr_api.flickrerrors.FlickrAPIError, ex:
        print "Error getting Exif: %s - %s" % (ex.code, ex.message)
        return
    tags_file = '%s-tags.xml' % saved_to_file
    tf = codecs.open(tags_file, 'w', 'utf-8')
    tf.write(
        "<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>\n")
    for tag in tags:
        # TODO: I don't think this gets tags that have multiple children, like keywords
        tf.write('<%s:%s>%s</%s:%s>\n' % (
            tag.tagspace, tag.tag,
            tag.raw,
            tag.tagspace, tag.tag))
    tf.write('</rdf:RDF>\n')
    tf.close()
    subprocess.call(['exiftool', '-overwrite_original', '-tagsfromfile', tags_file, "%s.jpg" % saved_to_file])
    # TODO: Check exit code to see if successful


def save_photo(photo, save_path):
    this_save_path = os.path.join(save_path, photo.owner.username)
    if not os.path.exists(this_save_path):
        os.mkdir(this_save_path)
    save_filename = "%s %s" % (photo.title, photo.id)
    for bad_character in ['"', '!', '\\', '/', '\'', '?', ';', '&', '>', '<']: # quotes do bad things with exiftool cmd
        save_filename = save_filename.replace(bad_character, '')
    save_to_file = os.path.join(this_save_path, save_filename)
    if os.path.exists("%s.jpg" % save_to_file):
        print "File already downloaded - %s.jpg" % save_to_file
        return
    else:
        photo.getSizes()
        # check if video:
        if photo.sizes.get("Video Player"):
            print "Skipping video"
            # TODO: Handle videos
            return
        largest_size = photo._getLargestSizeLabel()
        page_url = photo.getPageUrl()
        print ", ".join([photo.owner.username, photo.title, largest_size, page_url])

        try:
            photo.save(save_to_file, size_label=largest_size)
            print "Saved to %s.jpg" % save_to_file
        except flickr_api.flickrerrors.FlickrError as ex:
            if ex.message == "The requested size is not available":
                print "%s not found" % largest_size
        save_exif(photo, save_to_file)


def get_photos_by_tag(tag_value):
    photos = flickr_api.Walker(flickr_api.Photo.search, tags=tag_value)
    print "%d photos found" % photos._info.total
    return photos


def get_favorite_photos(user=None):
    if user == None:
        user = flickr_api.test.login()
    photos = flickr_api.Walker(user.getFavorites)
    print "%d photos found" % photos._info.total
    return photos

def get_photos_of_user(user=None):
    if user == None:
        user = flickr_api.test.login()
    photos = flickr_api.Walker(user.getPhotosOf)
    print "%d photos found" % photos._info.total
    return photos

def api_key_check_create():
    # Check for API keys
    if not os.path.exists("flickr_keys.py"):
        print "Not Flickr API keys found. Go here to get them: https://www.flickr.com/services/api/keys"
        fk = open("flickr_keys.py", 'w')
        api_key = raw_input("API_KEY: ")
        api_secret = raw_input("API_SECRET: ")
        fk.write("API_KEY=\'%s\'" % api_key)
        fk.write("\n")
        fk.write("API_SECRET=\'%s\'" % api_secret)
        fk.close()


def auth_file_check(auth_file_path):
    if os.path.exists(auth_file_path):
        print "Auth file found!"
        flickr_api.set_auth_handler(auth_file_path)
    else:
        print "No auth file found, please run 'python auth.py'"
        exit()


if __name__=="__main__":
    api_key_check_create()
    auth_file_check(".auth.txt")

    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)

    for photo in get_photos_of_user():
        save_photo(photo, SAVE_PATH)
    for photo in get_favorite_photos():
        save_photo(photo, SAVE_PATH)
    for photo in get_photos_by_tag("edrabbit"):
        save_photo(photo, SAVE_PATH)
