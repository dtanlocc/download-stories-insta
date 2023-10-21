from data_instagram import data_instagram

if __name__=='__main__':
    username = input('Enter username: ')
    data = data_instagram(username)
    choose = int(input("""          Cac lua chon:
          (1) Crawl stories in current day
          (2) Crawl full stories highlight
          Lua chon cua ban: """))
    if choose == 1:
        data.get_stories_username()
        print("Endtask!!!")
    else:
        data.get_all_stories_hightlight()
        print("Endtask!!!")
