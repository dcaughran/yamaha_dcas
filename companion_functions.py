from pythonosc.udp_client import SimpleUDPClient
from math import floor
from time import sleep
import socket

# Make sure editor is set up to link channel select with the console 

class yamahaQLCL:
  # Pages
  page_names = ["scratch1", # 1
                  "scratch2", # 2
                  "Channel Select", # 3
                  "Channel ON", # 4
                  "Channel OFF", # 5
                  "Labels", # 6
                  "DCA1 ON", # 7
                  "DCA1 OFF", # 8
                  "DCA2 ON", # 9
                  "DCA2 OFF", # 10
                  "DCA3 ON", # 11
                  "DCA3 OFF", # 12
                  "DCA4 ON", # 13
                  "DCA4 OFF", # 14
                  "DCA5 ON", # 15
                  "DCA5 OFF", # 16
                  "DCA6 ON", # 17
                  "DCA6 OFF", # 18
                  "DCA7 ON", # 19
                  "DCA7 OFF", # 20
                  "DCA8 ON", # 21
                  "DCA8 OFF", # 22
                  "Store 0", # 23
                  "Store 1", # 24
                  "Store 2", # 25
                  "Store 3", # 26
                  "Store 4", # 27
                  "Store 5", # 28
                  "Store 6", # 29
                  "Store 7", # 30
                  "Store 8", # 31
                  "Store 9", # 32
                  "Load 0", # 33
                  "Load 1", # 34
                  "Load 2", # 35
                  "Load 3", # 36
                  "Load 4", # 37
                  "Load 5", # 38
                  "Load 6", # 39
                  "Load 7", # 40
                  "Load 8", # 41
                  "Load 9", # 42
                  "DCA1 Color", # 43
                  "DCA2 Color", # 44
                  "DCA3 Color", # 45
                  "DCA4 Color", # 46
                  "DCA5 Color", # 47
                  "DCA6 Color", # 48
                  "DCA7 Color", # 49
                  "DCA8 Color"] # 50  
  
  wait_time = 0.02
    
    
  def __init__(self, port = 12321, ip = "127.0.0.1"):
    #ip = "1.1.1"
    self.ip = ip
    self.port = port
    print(ip)
    print(port)
    # OSC
    self.client = SimpleUDPClient(ip, port)  # Create client
    
    # Generic UDP
    self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    
    #client.send_message("/some/address", 123)   # Send float message

  def send_udp(self, message):
    self.client.sendto(bytes(message, "utf-8"), (self.ip, self.port))

  def send_osc(self, message):
    self.client.send_message(message, [])
      
      
  def press_button(self, page, key):
    # OSC  
    #self.send_osc("/press/bank/%d/%d"%(page, key))
    
    self.send_udp("BANK-PRESS %d %d"%(page+1, key))
    sleep(self.wait_time)
    
  def set_variable(self, name, value):
    # OSC
    #self.send_osc("/custom-variable/%s %s"%(name, value))
    
    # UDP
    self.send_udp("CUSTOM-VARIABLE %s SET-VALUE %s"%(name, value))
    sleep(self.wait_time)


  def select_channel(self, channel):
    page = self.page_names.index("Channel Select")
    key = channel
    self.press_button(page, key)

  def channel_enable(self, channel, state):
      if state:
          page = self.page_names.index("Channel ON")
      else:
          page = self.page_names.index("Channel OFF")
              
      key = channel
      self.press_button(page, key)
      
  def dca_set(self, dca, channel, state):
      if state:
          page = self.page_names.index("DCA%d ON"%dca)
      else:
          page = self.page_names.index("DCA%d OFF"%dca)
              
      key = channel
      self.press_button(page, key)
      
  def scene_store(self, scene):
      scene_bank = floor(scene / 32)
      key = scene % 32
      page = self.page_names.index("Store %d"%scene_bank)

      self.press_button(page, key)
      
  def scene_recall(self, scene):
      scene_bank = floor(scene / 32)
      key = scene % 32
      page = self.page_names.index("Load %d"%scene_bank)

      self.press_button(page, key)
      
  def dca_color(self, dca, color = 'Off'):
      # Allowable colors
      dca_colors = ['Blue', 
                    'Orange',
                    'Yellow',
                    'Purple',
                    'Cyan',
                    'Magenta',
                    'Red',
                    'Green',
                    'Off']

      
      if color == '':
          color = 'Off'
          
      page = self.page_names.index("DCA%d Color"%dca)
      try:
          key = dca_colors.index(color)
          self.press_button(page, key+1)
      except:
          key = dca_colors.index('Yellow')
          print('bad color %s'%color)
      # TBD: Set DCA Color
      
  def dca_name(self, dca, name):
      self.set_variable('dca%d_name'%dca, name)
      page = self.page_names.index("Labels")
      
      
      
      # TBD: Set DCA name
      
  def scene_name(self, scene, name):
      self.set_variable('scene_name', name)
      page = self.page_names.index("Labels")
      
      # TBD: Set scene name
      

if __name__ == "__main__":
  #console = yamahaQLCL(ip = '127.0.0.1')
  console = yamahaQLCL(port = 16759, ip = '127.0.0.1')
  #console.select_channel(2)
  console.press_button(6, 32)
  console.set_variable("dca1_name", "ME!")
