import sys
import ipaddress
from IPy import IP


def IPs_big_to_little(big_IPs, little_num):
    '''Large IPv4 segments are divided into small segments.
    
    Args:
        big_IPs: A large IPv4 segments, such as "121.68.0.0/20".
        little_num: The number of small IPv4 segments network bit such as "24".
        
    Returns: Small segments list.
    '''
    
    little_IP_list = []
    middle_bin_list = []
    big_IPs = ipaddress.ip_network(big_IPs , strict=False)  # normalized IP segments 
    big_IP_str_list = str(big_IPs).split('/')               # '121.68.0.0/20'-> '20' 
    start_num = IP(big_IP_str_list[0]).strBin()[int(big_IP_str_list[1]):little_num]
    little_IPs_num = 2**len(start_num)
    
    # Generate the middle network bit
    while little_IPs_num > 0:   
        middle_bin_list.append(start_num)
        start_num = add_binary_nums(start_num, '1')
        little_IPs_num = little_IPs_num - 1
        
    IPs_big_start = IP(big_IP_str_list[0]).strBin()[0:int(big_IP_str_list[1])]   # small segments and large segments common network bit
    
    # Because small IPv4 segments  not up 32 bits,so complement IP address with zero 
    last_zero_str = '0' * (32 - little_num)
    #k = 32 - little_num
    #while k > 0:
        #last_zero_str += '0'
        #k = k - 1
    
    # Splicing into a complete small segments list
    for j in middle_bin_list:
        IP_little_bit_one =  IPs_big_start + j + last_zero_str
        IP_little_one = str(ipaddress.ip_address(int(IP_little_bit_one, 2))) + '/' + str(little_num)
        little_IP_list.append(IP_little_one)
    return little_IP_list


def add_binary_nums(x, y):  
    ''' Addition of two binary numbers.

    Args:
        x: One of binary numbers.
        y: One of binary numbers.
        
    Returns: The sum of two binary numbers
    '''
    
    max_len = max(len(x), len(y))  
    x = x.zfill(max_len)  
    y = y.zfill(max_len)  
    result = ''  
    carry = 0  
    for i in range(max_len-1, -1, -1):  
        r = carry  
        r += 1 if x[i] == '1' else 0  
        r += 1 if y[i] == '1' else 0  
        result = ('1' if r % 2 == 1 else '0') + result  
        carry = 0 if r < 2 else 1         
    if carry !=0 : result = '1' + result  
    return result.zfill(max_len)     


if __name__ == '__main__':
    little_IP_list = IPs_big_to_little(sys.argv[1], int(sys.argv[2]))
    print(little_IP_list)
    print(len(little_IP_list))
    
    # check the function of IPs_big_to_little
    for ips in little_IP_list:
        if not ips in IP(str(ipaddress.ip_network(sys.argv[1], strict=False))):
            print(ips)