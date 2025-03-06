import urllib.request as libreq

link1 = "http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1"
link2 = "https://export.arxiv.org/api/query?search_query=au:markovitch&max_results=100"

results_fn = 'results.txt'
links_fn = 'links.txt'

#1 entry
with libreq.urlopen(link1) as url:
    r = url.read()
#multiple entries
with libreq.urlopen(link2) as url:
    a = url.read()

#write the initial results into a file
#multiple entries
with open(results_fn, "wb") as file:
    file.write(a)

#find the link in the id tag
id_tag = b"<id>"
link_result = b""
all_links = []
with open(results_fn, "rb") as file:
    data = file.read()
    #find multiple instances of id_tag
    all_id_tags = []
    pos = data.find(id_tag)
    while pos != -1:
        all_id_tags.append(pos)
        pos = data.find(id_tag, pos+1)
    #save the bytes of the links 
    for i in all_id_tags:
        file.seek(i+len(id_tag))
        subsequent_data = file.read(1)
        end_of_link = b"<"
        while(subsequent_data != end_of_link):
            link_result += subsequent_data
            subsequent_data = file.read(1)
        #dont save api link
        if b'api' in link_result:
            link_result = b""
        else: 
            all_links.append(link_result)
        link_result = b""

#CLEAN THE LINKS
# assuming all the links have a pdf format
# swap all instances of the 'abs' bytes into 'pdf' 
# to ensure entire pdf version of paper is found instead of the abstract
for i in range(len(all_links)):
    pdf_handle = b'pdf'
    target_handle = b'abs'
    all_links[i] = all_links[i].replace(target_handle, pdf_handle)

#save the link to a list file. 
with open(links_fn, "wb") as file:
    for link in all_links:
        file.write(link)
        file.write(b"\n")

