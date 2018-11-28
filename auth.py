import flickr_api

a = flickr_api.auth.AuthHandler() # creates a new AuthHandler object
perms = "read" # set the required permissions
url = a.get_authorization_url(perms)
print "Go to this URL: %s" % url # this is the url we need!

print "You'll need the <oauth_verifier> value from the XML returned in the browser"
verifier_code = raw_input("What's the oauth_verifier value? ")
a.set_verifier(verifier_code)
flickr_api.set_auth_handler(a) # set the AuthHandler for the session
a.save(".auth.txt")