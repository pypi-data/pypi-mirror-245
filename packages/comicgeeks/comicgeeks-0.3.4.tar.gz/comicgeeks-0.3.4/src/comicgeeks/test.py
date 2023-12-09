from comicgeeks import Comic_Geeks

client = Comic_Geeks()

s = client.issue_info(4090926)

print(s.variant_covers)
