def LogToHtml(file_name, html_name):
  f = open(file_name)
  all_log = f.read()
  f.close()
  
  lines = all_log.split(";\n")[1:]
  #print(lines) 
  talks = []
  for l in lines[:-1]:
    msg_dict = {}
    messages = l.split(",")
    print(messages)
    msg_dict["You"] = messages[0].replace('\n', '<br>')
    msg_dict["System"] = messages[1].replace('\n', '<br>')
    talks.append(msg_dict)
  '''
  for t in talks:
    print(t)
    print()
  '''
  output = open(html_name, 'w')
  head = '<link rel="stylesheet" type="text/css" href="css/style.css">\n<div id="chat-frame">'
  bottom = '</div>'

  output.write(head)
  for t in talks:
    your_chat_frame = '<p class="chat-talk mytalk">\n\t<span class="talk-icon">\n\t\t<img src="icon/myicon.jpg" alt="myicon" width="XX" height="XX"/>\n\t</span>\n\t<span class="talk-content">%s</span>\n</p>' % (t["You"])
    output.write(your_chat_frame)
    system_chat_frame = '<p class="chat-talk">\n\t<span class="talk-icon">\n\t\t<img src="icon/targeticon.png" alt="tartgeticon" width="XX" height="XX"/>\n\t</span>\n\t<span class="talk-content">%s</span>\n</p>' % (t["System"])
    output.write(system_chat_frame)
  output.write(bottom)
  output.close()

if __name__ == '__main__':
  input_file = input(">> ")
  file_name = "./LOG/" + input_file
  html_name = "./LOG/design/" + input_file[:-4] + ".html"
  LogToHtml(file_name, html_name)
