##ONLY DELETE THIS FILE WHEN API WORKS##

If you're reading this, you are most likely viewing the "tapo-p110-integration" branch of the main repository

The main branch exists as a virtual-only implementation. That is, all of it uses simulated-only values and doesn't actually interface with any hardware.
Everything on the main branch works, but the api isn't fully implemented yet.

THIS branch though, attempts to provide an easy and intuitive integration of the tapo p110 plugs by extending the functions of the (previously simulated) 
device object by making it a child class of the interface object provided in the updated tapo api library by almottier on GitHub. His work is the sole reason this project works at all.
it saves us from having to waste untold hours reverse engineering the tapo api ourselves (all of the commonly available libraries are out of date and DO NOT WORK.)
you will need to install his library with this command => pip install git+https://github.com/almottier/TapoP100.git@main

Anyway, some things aren't yet implemented on this version of the repository code:
- The API routes in decisionmaker.py and priority.py have not yet been changed to reflect the changes to the Device object defined in priority.py 
    (I would recommend updating the api routes before trying to use them, or you may encounter crashes and other voodoo weirdness)
- The API class interface (interface.py) isn't properly implemented yet. Each method provided by that class should send a single http request that corresponds with one of the api routes
    (it is basically an easy and in-code way to invoke the api without having to use httpie or command line every time)
- The data capturing of priority.py (for creating devices with data input captured from terminal) hasn't been updated to work with the new virtual device object.

It is a simple fix that i unfortunately don't have the time for currently. just replace the object values used for testing ("energy", "state") that are referenced in the api.
some new functions are included in the object class that serve these same purposes, but for real hardware. they use the same function names i think.

Also, some things to note:
- The only files actually involved in "running" the system are priority.py, decisionmaker.py, and simulatedmeterclass.py in /metermodule/
- the two demo files in the metermodule folder can be deleted, but they illustrate two ways on changing the simulated solar power production values of the system.
- plug_controller.py illustrates how almottier's library works. this is what actually lets us communicate with tapo's plugs 
    (the tapo plugs have some stupid esoteric proprietary api. that they break every 6 months with firmware updates. the official libraries of openhab DO NOT WORK.)
- you will need to download his library manually with this command => pip install git+https://github.com/almottier/TapoP100.git@main
    (after this, you can run our files)
- plugtest.py uses our virtual device object that contains some extended functions.
- the main program loop is located within "decisionmaker.py". run that file for things to happen.
- device information is stored persistently between sessions in a json text database, "exported_devices.json"
- normally these virtual devices are saved to text with the json_export function in priority.py, and loaded and reconstructed from text with the json_parse function.
- as mentioned above, the data capturing of priority.py doesn't work so creating devices will be a little more difficult.
- feel free to just copy the format of the devices already in the database. it should look something like this:

== ON THE ALGORITHM
{"plugip": "192.168.0.1", "accountemail": "blabla@email.com", "accountpassword": "password123", "name": "Lamp Plug 1", "priority": "1", "typicalconsumption": "100"}
- plug ip should be a valid local ipv4 address, pointing towards the desired plug
- accountemail is the address email associated your tapo cloud account (i think this is used to verify the requests it receives. no email is sent).
- accountpassword is the password of your tapo cloud account (see above. make sure 2FA is disabled on your tapo account)
- name is any name that will help you remember what the plug is for. i recommend giving it a number too.
- priority is the priority value that is used by my algorithm. this should be an integer from 1 to 5. priority 1 devices are turned off first and turned back on last. 
    (the higher the priority, the more we try to keep it on)
- typicalconsumption is any number that represents the typical consumption (in watts) of your device. this helps the algorithm decide if a device should be turned on or not.
    (if you dont know the typical consumption, you can just set this to zero)


to whoever you are working on this project next, good luck with your capstone work
and my sincere apologies for my messy code.

sincerely, team #1 of semester 1 2024
david (me), mayank, alex, alan, grace

##ONLY DELETE THIS FILE WHEN API WORKS##