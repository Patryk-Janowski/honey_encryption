import random
import re


def parse_passwd_list(path):
    p_list = list()
    count_pattern = re.compile(r'\.\s+(\d+)')
    password_pattern = re.compile(r'\b\w+$')
    total_count = 0

    with open(path) as f:
        for line in f.readlines():
        
            count = count_pattern.search(line)
            passwd = password_pattern.search(line)

            if passwd and count:
                count = int(count.group(1))
                p_list.append([passwd.group(), count])
                total_count += count
    
    return p_list, total_count


def get_prob_list(p_list, total_count):
    return [(passwd, count/total_count) for passwd, count in p_list]


def get_numbererd_list(prob_list, n):
    n_list = [[passwd, round(prob * n)] for passwd, prob in prob_list]
    n_list = sorted(n_list, key=lambda x: x[1], reverse=True)
    s = sum(map(lambda x: x[1], n_list))

    diff = s - n
    l = len(n_list)

    if diff > 0:
        for i in range(diff):
            n_list[i][1] -= 1
    elif diff < 0:
        for i in range(abs(diff)):
            n_list[l-i-1][1] += 1

    return sorted(n_list, key=lambda x: x[1], reverse=True)


def get_mapping_message_to_seed(n_list, n):
    nums = [x for x in range(n)]
    random.shuffle(nums)
    i = 0
    message_to_seed = list()

    for passwd, num in n_list:
        mess_map = list()
        for _ in range(num):
            mess_map.append(nums[i])
            i += 1
        message_to_seed.append([passwd, mess_map])

    return message_to_seed


def get_mapping_seed_to_message(message_to_seed, n):
    seed_to_message = [[x] for x in range(n)]
    for passwd, mess_map in message_to_seed:
        for i in mess_map:
            seed_to_message[i].append(passwd)

    return seed_to_message


def decode(seed, seed_to_message):
    return seed_to_message[seed][1]


def encode(message, message_to_seed):
    i = list(map(lambda x: x[0], message_to_seed)).index(message)
    return random.choice(message_to_seed[i][1])


def encode_password(password, n):
    return hash(password) % n


def encrypt(message, password, message_to_seed, n):
    p_seed = encode_password(password, n)
    m_seed = encode(message, message_to_seed)
    return p_seed ^ m_seed


def decrypt(cipher, password, seed_to_message, n):
    p_seed = encode_password(password, n)
    return decode(p_seed ^ cipher, seed_to_message)


if __name__ == '__main__':
    n = 256
    p_list, total_count = parse_passwd_list('common_passwords.txt')
    prob_list = get_prob_list(p_list, total_count)
    n_list = get_numbererd_list(prob_list, n)
    message_to_seed = get_mapping_message_to_seed(n_list, n)
    seed_to_message = get_mapping_seed_to_message(message_to_seed, n)
    passwd = 'jan watykan'
    cipher = encrypt('adobe123', passwd, message_to_seed, n)
    mess = decrypt(cipher, '11', seed_to_message, n)
    print(mess)
