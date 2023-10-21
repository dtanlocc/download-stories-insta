import requests
from tqdm import tqdm
import os
from datetime import datetime

class data_instagram:
    def __init__(self,username) -> None:
        self.username = username
        self.account = 'https://storiesig.info/api/ig/userInfoByUsername/' + self.username
        self.instagram = f'https://www.instagram.com/stories/{self.username}/'
        

    def create_folder_save(self,flag = 0,title=''): #flag=0 -> create folder save stories current_data
        if flag ==0:
        # Lấy ngày tháng hiện tại
            current_date = datetime.now().strftime("%Y-%m-%d")

            # Tạo thư mục với tên theo ngày tháng hiện tại
            folder_name = os.path.join("downloads_stories", current_date)
            os.makedirs(folder_name, exist_ok=True)
            return folder_name
        #flag=1 -> create folder to save post
        else:
            folder_name = os.path.join(self.get_name(), title) 
            os.makedirs(folder_name, exist_ok=True)
            return folder_name
            

    
    def download_video(self,url,filename,type='Video'):
        self.url_download = url
        self.video_path = filename
        # Tải video từ URL
        response = requests.get(self.url_download, stream=True)

        if response.status_code == 200:
            # Lấy kích thước tệp video
            total_size = int(response.headers.get('content-length', 0))

            # Sử dụng tqdm để theo dõi tiến trình tải xuống
            with open(self.video_path, "wb") as video_file, tqdm(
                total=total_size, unit="B", unit_scale=True, unit_divisor=1024
            ) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    video_file.write(data)
                    progress_bar.update(len(data))

            print(f"{type} đã được tải xuống thành công.")
        else:
            print(f"Không thể tải xuống {type}. Mã trạng thái:", response.status_code)

    def get_stories_username(self):
        folder_name = self.create_folder_save(flag=0)
        url = f'https://storiesig.info/api/ig/story?url={self.instagram}'
        self.get_stories(url=url,folder_name=folder_name)

    # def get_stories(self,url,folder_name):
    #     respones = requests.get(url)
    #     json_stories = respones.json()
    #     number = 1
    #     for element in json_stories['result']:
    #         ele = dict(element['video_versions'][0])
    #         link_download = ele['url']
    #         video_filename = f"video{number}.mp4"
    #         video_path = os.path.join(folder_name, video_filename)
    #         self.download_video(url=link_download,filename=video_path)
    #         number+=1

    # def get_pic(self,url,folder_name):
    #     respones = requests.get(url)
    #     json_stories = respones.json()
    #     number = 1
    #     for element in json_stories['result']:
    #         ele = dict(dict(element['image_versions2']['candidates'][0]))
    #         link_download = ele['url']
    #         video_filename = f"picture{number}.jpg"
    #         video_path = os.path.join(folder_name, video_filename)
    #         self.download_video(url=link_download,filename=video_path)
    #         number+=1

    def get(self,url,folder_name):
        respones = requests.get(url)
        json_stories = respones.json()
        number_video = 1
        number_picture = 1
        for element in json_stories['result']:
            try:
                ele = dict(element['video_versions'][0])
                link_download = ele['url']
                video_filename = f"video{number_video}.mp4"
                video_path = os.path.join(folder_name, video_filename)
                self.download_video(url=link_download,filename=video_path,type='Video')
                number_video+=1
            except:
                ele = dict(dict(element['image_versions2']['candidates'][0]))
                link_download = ele['url']
                video_filename = f"picture{number_picture}.jpg"
                video_path = os.path.join(folder_name, video_filename)
                self.download_video(url=link_download,filename=video_path,type='Picture')
                number_picture+=1
            
            


    def get_user_id(self):
        res = requests.get(self.account)
        html = res.json()
        return html['result']['user']['pk']

    def get_name(self):
        res = requests.get(self.account)
        html = res.json()
        return html['result']['user']['full_name']

    def get_all_stories_hightlight(self):
        user_id = self.get_user_id()
        self.hightlight = f'https://storiesig.info/api/ig/highlights/{user_id}'
        res = requests.get(self.hightlight)
        data = res.json()
        for element in data['result']:
            ele = element['id']
            print(f'Crawl data from highlight id {ele}')
            title = element['title']
            url = f'https://storiesig.info/api/ig/highlightStories/{ele}'
            print(url)
            folder_name = self.create_folder_save(flag=1,title=title)
            self.get(url=url,folder_name=folder_name)
            print(f'---------------------------------------------End------------------------------------------')
            
