from flask import Flask, render_template, request
import subprocess
import re


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
    return render_template('mac_changer.html')

@app.route('/mac_changer_result', methods = ['GET','POST'])
def macChangerResult():
    #interfaces = ['eth0','eth1','eth2','wlan0','wlan1','wifi0','ath0','ath1','ppp0']
    if request.method == 'POST':
        interface = request.form['interface']
        macAddress = request.form['mac_address']
        
        if interface == '' or macAddress == '':
            return 'Do not leave the fields blank.'

        #if interface in interfaces:
            #pass
        #else:
            #return 'Enter one of the interfaces available in Kali Linux.'

        splitMacAddress = macAddress.split(':')
        for splitMacAddress_ in splitMacAddress:
            if len(splitMacAddress_) == 2:
                pass
            else:
                return 'Please enter a correct mac address.'

        changeMacAddress(interface, macAddress)
        finalizedMac = controlNewMac(str(interface))
        if finalizedMac == macAddress:
            return 'Mac Address changed successfully.'
        else:
            return 'Could not change Mac Address.'

    else:
        return 'For post requests only.'


def changeMacAddress(user_interface,user_mac_address):
    subprocess.call(['ifconfig',user_interface,'down'])
    subprocess.call(['ifconfig', user_interface,'hw','ether',user_mac_address])
    subprocess.call(['ifconfig',user_interface,'up'])

def controlNewMac(interface):
    ifconfig = subprocess.check_output(['ifconfig',interface])
    newMac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',str(ifconfig))

    if newMac:
        return newMac.group(0)
    else:
        return None



if __name__ == '__main__':
    app.run(debug=True, port=5000)
