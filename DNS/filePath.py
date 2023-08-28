import os
import shutil
from jinja2 import Template
from configFile import namedConfFile
step_1 = "Network ip config Done ???"
step_2 = "Hostname edit Done /etc/hostname file ???"
step_3 = "Static Hostname edit Done /etc/hosts file ???"
step_4 = "bind package install Done ???"
step_5 = "resolv file edit Done /etc/resolv.conf???\n####example\nsearch example.com\nnameserver 192.168.0.100\n"
step_6 = "Static Hostname edit Done /etc/hosts file ???"
step_7 = "listen-on port 53 Host Machine or any ???"
step_8 = "allow-query local subnet or any ???"
step_9 = "forward zone add enter forward zone name: "
step_10= "reverse zone add enter reverse zone name: "

print(f"{step_1}Then Press 1" )
print("Step 1 >>>>> named.conf File Edit")
# hostIp = input("Enter Host Machine ip Address: ")
def dnsConfig(hostIp="any", allow_query="any",):
        try:
            template = Template(namedConfFile)
            config = template.render(hostIp=hostIp)
            # print(config)
            filename = "named.conf"
            with open(f"/etc/named.conf", "w", encoding='utf-8') as f:
                # with open(filename, "w", encoding='utf-8') as f:
                f.write(config)
            print(f"File '{filename}' created successfully.")
        # except PermissionError:
        #     print("Error: Permission denied. Program Run Root User Otherwise Not work This Program")
        except Exception as e:
            print(f"Error creating the file: {e}\nplease program run root user")


step_1_Userinput = input("Step 1: Do you want to proceed? (yes/no): ")

if step_1_Userinput.lower() == "yes":
    print("Step 1: pass")
    step_2_Userinput = input("Step 2: Do you want to proceed? (yes/no): ")

    if step_2_Userinput.lower() == "yes":
        print("Step 2: pass")
        step_3_Userinput = input("Step 3: Do you want to proceed? (yes/no): ")

        if step_3_Userinput.lower() == "yes":
            print("Step 3: pass")
            # Continue the pattern for the remaining steps
            step_4_Userinput = input("Step 4: Do you want to proceed? (yes/no): ")

            if step_4_Userinput.lower() == "yes":
                print("Step 4: pass")
                step_5_Userinput = input("Step 5: Do you want to proceed? (yes/no): ")

                if step_5_Userinput.lower() == "yes":
                    print("Step 5: pass")
                    step_6_Userinput = input("Step 6: Do you want to proceed? (yes/no): ")

                    if step_6_Userinput.lower() == "yes":
                        print("Step 6: pass")
                        step_7_Userinput = input("Step 7: Do you want to proceed? (yes/no): ")

                        if step_7_Userinput.lower() == "yes":
                            print("Step 7: pass")
                            step_8_Userinput = input("Step 8: Do you want to proceed? (yes/no): ")

                            if step_8_Userinput.lower() == "yes":
                                print("Step 8: pass")
                                step_9_Userinput = input("Step 9: Do you want to proceed? (yes/no): ")

                                if step_9_Userinput.lower() == "yes":
                                    print("Step 9: pass")
                                    step_10_Userinput = input("Step 10: Do you want to proceed? (yes/no): ")

                                    if step_10_Userinput.lower() == "yes":
                                        print("Step 10: pass")
                                    else:
                                        print("Step 10: not proceeding")
                                else:
                                    print("Step 9: not proceeding")
                            else:
                                print("Step 8: not proceeding")
                        else:
                            print("Step 7: not proceeding")
                    else:
                        print("Step 6: not proceeding")
                else:
                    print("Step 5: not proceeding")
            else:
                print("Step 4: not proceeding")
        else:
            print("Step 3: not proceeding")
    else:
        print("Step 2: not proceeding")
else:
    print("Step 1: not proceeding")



# dnsConfig(hostIp=hostIp)