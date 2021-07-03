launch server on a machine, specify machine name or IP and port :
`TCP_paint_server.py 192.168.1.17 55555`
launch client on same or other machine specify server machine name and port:
`TCP_paint_client.py 192.168.1.17 55555`

select 1 for new "paint game"
2 for joining existing game.
Server can support many clients.
Each new game has a "thread" name. If you wish to join game you have to specify the exact thread name as follow:
`Thread-2`

![sampleimage](./TCPpaintGUI1.png)
![sampleimage](./TCPpaintGUI2.png)
![sampleimage](./TCPpaintGUI3.png)
