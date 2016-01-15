def sign_request(raw):
    from hashlib import sha1
    import hmac

    # key = CONSUMER_SECRET& #If you dont have a token yet
    key = "84d415a6d1bae8f29bf629346d4b275e"

    hashed = hmac.new(key, raw, sha1)

    # The signature
    return hashed.digest().encode("hex")