# mmsend/mmrecv
## Easily transfer files to/from a Picomite over USB serial Mac
#### Requires Python and the xmodem python module

### 

### Prelude

This is a fork of <a href="https://github.com/gruvin/mmxmodem">gruvin/mmxmodem</aa>

It modifies the original to use Python3 to use the pypi.org  <a href="http://packages.python.org/xmodem">xmodem</a> package

This code is designed to send/receive files to/from   <a href="https://geoffg.net/picomite.html">Picomite</a> running on a Raspberry Pi Pico. 

### Script Scope

Under Windows, one may use TeraTerm to emulate a VT100 terminal (for which MM-Basic is designed) as serial console. Files can be easily transferred using MM-BASIC's _XMODEM SEND/RECEIVE_ commands and TeraTerm's corresponding built-in Xmodem file transfer features. However ...

However in a MacOS envirnoment terminal emulation can be easily acheived using the Mac native terminal emulator iTerm or the 3rd party iTerm2 and ```screen```. These don't have built it support for XMODEM.


The  ```mmsend.py``` and ```mmrecv.py``` -- Python scripts allow sending and receiving files with out having to load a 3rd party linux/BCD module like lrzsz.

    Usage: mmsend.py <serial-port> <filename> [<dest-filename>]

and

    Usage: mmrecv.py <serial-port> <source-filename> [<local-filename>]

Example: ```./mmsend.py /dev/ttyACM0 foo.bas wahoo.bas```

Sample session -- Mac Shell ...

    % ./mmsend /dev/ttyACM0 foo.bas wahoo.bas
    MM-BASIC connected. Setting up XMODEM transfer ...
    Sending  foo.bas as wahoo.bas ...
    Done!

Sample session -- Windows Command Prompt ...

    C:\Users\Gruvin\mmxmodem> mmsend com3 foo.bas wahoo.bas
    MM-BASIC connected. Setting up XMODEM transfer ...
    Sending  foo.bas as wahoo.bas ...
    Done!

### Notes

* All files are transferred in binary mode. No CR/LF translation is attempted for text files. But MMBasic handles that OK.
* Wildcards (multiple files) are NOT handled (on either end). Thus, ```mmrecv /dev/tty/ACM0 *.BAS``` will *not* work.
* Received files often have trailing null characters on the end. I believe this is a bug at the Maximite end -- possibly related to the "A:" drive internal block size or something. (I'm really just guessing.) In any case, I can't really strip them off, because a non-".BAS" file may well have appended null chars intentionally.



#### You do NOT need to initiate XMODEM on the Picomite.

You do have to quit all attached screens because these scripts require sole access to the USB serial port.

The scripts take care of initialising the ```xmodem send/receive``` at the Picomite end. When you're done transferring files, simply re-launch screen and carry on with the Picomite from where you left off.





