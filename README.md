# Micrscope software

## Terminology

 * **scope** - the software running on the Raspberry Pi. Plan: Flask server responsible for:
    * Controlling the movement of the stepper motors
    * Publishing stepper motor status via MQTT
    * Recieving commands from client
    * Recieving commands from 3DSpaceMouse
 * **client** - the software running on local computer. responsible for:
    * Managing MQTT queue
    * YOLO8 tracking
    * Camera livestream management
    * Sending commands to scope
    * Providing subscription to Grafane
 * **grafana** - the dashboard that interfaces with the client
    * Subscribes to data from the client
    * Hits client endpoints to control scope



## Rough notes
### Raspberry Pi
To login `ssh pi@raspberrypi.local`
To edit startup `sudo crontab -e`
Include in crontab: `@reboot sh /home/pi/workspace/microscope-control/run_scope.sh > /home/pi/workspace/microscope-control/logs/cronlog 2>&1`
### Stepper motors
1600 pulse/rev (off on off) works well

### Graphana
run `./run_graphana.sh` to start
go to localhost:3000/login

### client
run `./run_client.sh` to start
go to 
