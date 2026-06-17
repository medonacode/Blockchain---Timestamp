from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
import shutil
from PIL import Image
from datetime import datetime
from datetime import date

import pywintypes
import win32file
import win32con
import datetime
import platform

import json
import re
import random
import cv2
from random import seed
from random import randint
from werkzeug.utils import secure_filename
from flask import send_file
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import threading
import time
import shutil
import platform
import hashlib
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser


#drive

#ip,mac
import socket
import re, uuid
#dir
import subprocess

from Crypto.Hash import SHA256
from Crypto import Random
import sys


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="time_miner"
)

app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####

@app.route('/',methods=['POST','GET'])
def index():
    msg=""

    
    return render_template('index.html',msg=msg)

@app.route('/login',methods=['POST','GET'])
def login():
    act=request.args.get("act")
    msg=""
   
    if request.method == 'POST':
        
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM tm_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
          
            return redirect(url_for('home')) 
        else:
            msg="You are logged in fail!!!"
        

    return render_template('login.html',msg=msg,act=act)

@app.route('/home', methods=['GET', 'POST'])
def home():
    msg=""
    act=""
    mycursor = mydb.cursor()
            
    mycursor.execute("SELECT * FROM tm_register where id=1")
    data = mycursor.fetchone()   
    
    return render_template('web/home.html', act=act,msg=msg,data=data)


@app.route('/add_config', methods=['GET', 'POST'])
def add_config():
    msg=""
    act=""
    mycursor = mydb.cursor()

    mac=':'.join(re.findall('..', '%012x' % uuid.getnode()))

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    IP = socket.gethostbyname(hostname)

    if request.method=='POST':
        name=request.form['name']
        
        mobile=request.form['mobile']
        email=request.form['email']
        ipaddr=request.form['ipaddr']
        macaddr=request.form['macaddr']
        
        mycursor.execute("SELECT count(*) FROM tm_register")
        myresult = mycursor.fetchone()[0]

        if myresult==0:
            
            mycursor.execute("SELECT max(id)+1 FROM tm_register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            sql = "INSERT INTO tm_register(id,name,mobile,email,create_date,ip_address,mac_address) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = ('1',name,mobile,email,rdate,ipaddr,macaddr)
            mycursor.execute(sql, val)
            mydb.commit()

         
            msg="success"
        else:
            mycursor.execute("update tm_register set name=%s,mobile=%s,email=%s,ip_address=%s,mac_address=%s where id=1",(name,mobile,email,ipaddr,macaddr))
            msg="success"
            
    mycursor.execute("SELECT * FROM tm_register where id=1")
    data = mycursor.fetchone()   
    
    return render_template('web/add_config.html', act=act,msg=msg,IP=IP,mac=mac,data=data)


def calculate_hash(file_path):
    # Calculate the hash value of a file
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)  # Read the file in chunks to avoid loading it entirely into memory
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

#Blockchain
class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         
        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200



def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

def timechain(uid,uname,bcdata,utype):
    ############

    now = datetime.datetime.now()
    yr=now.strftime("%Y")
    mon=now.strftime("%m")
    rdate=now.strftime("%d-%m-%Y")
    rtime=now.strftime("%H:%M:%S")
    
    ff=open("static/key.txt","r")
    k=ff.read()
    ff.close()
    
    #bcdata="CID:"+uname+",Time:"+val1+",Unit:"+val2
    dtime=rdate+","+rtime

    ff1=open("static/web/js/d1.txt","r")
    bc1=ff1.read()
    ff1.close()
    
    px=""
    if k=="1":
        px=""
        result = hashlib.md5(bcdata.encode())
        key=result.hexdigest()
        print(key)
        v=k+"##"+key+"##"+bcdata+"##"+dtime

        ff1=open("static/web/js/d1.txt","w")
        ff1.write(v)
        ff1.close()
        
        dictionary = {
            "ID": "1",
            "Pre-hash": "00000000000000000000000000000000",
            "Hash": key,
            "utype": utype,
            "Date/Time": dtime
        }

        k1=int(k)
        k2=k1+1
        k3=str(k2)
        ff1=open("static/key.txt","w")
        ff1.write(k3)
        ff1.close()

        ff1=open("static/prehash.txt","w")
        ff1.write(key)
        ff1.close()
        
    else:
        px=","
        pre_k=""
        k1=int(k)
        k2=k1-1
        k4=str(k2)

        ff1=open("static/prehash.txt","r")
        pre_hash=ff1.read()
        ff1.close()
        
        g1=bc1.split("#|")
        for g2 in g1:
            g3=g2.split("##")
            if k4==g3[0]:
                pre_k=g3[1]
                break

        
        result = hashlib.md5(bcdata.encode())
        key=result.hexdigest()
        

        v="#|"+k+"##"+key+"##"+bcdata+"##"+dtime

        k3=str(k2)
        ff1=open("static/key.txt","w")
        ff1.write(k3)
        ff1.close()

        ff1=open("static/web/js/d1.txt","a")
        ff1.write(v)
        ff1.close()

        
        
        dictionary = {
            "ID": k,
            "Pre-hash": pre_hash,
            "Hash": key,
            "utype:": utype,
            "Date/Time": dtime
        }
        k21=int(k)+1
        k3=str(k21)
        ff1=open("static/key.txt","w")
        ff1.write(k3)
        ff1.close()

        ff1=open("static/prehash.txt","w")
        ff1.write(key)
        ff1.close()

    m=""
    if k=="1":
        m="w"
    else:
        m="a"
    # Serializing json
    
    json_object = json.dumps(dictionary, indent=4)
     
    # Writing to sample.json
    with open("static/timechain.json", m) as outfile:
        outfile.write(json_object)
    ##########

#Leighton-Micali Signatures (LMS)
def H(x):
#    print "hash input: " + stringToHex(x)
    h = SHA256.new()
    h.update(x)
    return h.digest()[0:n]

def sha256_iter(x, num):
    tmp = x
    for j in range(0, num):
        tmp = H(tmp + I + q + uint16ToString(i) + uint8ToString(j) + D_ITER)

# entropy source
#
entropySource = Random.new()

# integer to string conversion
#
def uint32ToString(x):
    c4 = chr(x & 0xff)
    x = x >> 8
    c3 = chr(x & 0xff)
    x = x >> 8
    c2 = chr(x & 0xff)
    x = x >> 8
    c1 = chr(x & 0xff)
    return c1 + c2 + c3 + c4

def uint16ToString(x):
    c2 = chr(x & 0xff)
    x = x >> 8
    c1 = chr(x & 0xff)
    return c1 + c2

def uint8ToString(x):
    return chr(x)

def stringToUint(x):
    sum = 0
    for c in x:
        sum = sum * 256 + ord(c)
    return sum

def stringToHex(x):
    return "".join("{:02x}".format(ord(c)) for c in x)

class LMSKeyPair:
    def __init__(self, height=4):
        self.h = height
        self.n = 2 ** height
        self.private_keys = [os.urandom(32) for _ in range(self.n)]
        self.leaves = [H(pk) for pk in self.private_keys]
        self.tree = self._build_merkle_tree(self.leaves)
        self.public_key = self.tree[0][0]  # Merkle root
        self.used = set()

    def _build_merkle_tree(self, leaves):
        tree = [leaves]
        level = leaves
        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                combined = level[i] + level[i + 1]
                next_level.append(H(combined))
            tree.insert(0, next_level)
            level = next_level
        return tree

    def get_auth_path(self, index):
        path = []
        for level in range(len(self.tree) - 1, 0, -1):
            sibling = index ^ 1
            path.append(self.tree[level][sibling])
            index //= 2
        return path
class LMSSignature:
    def __init__(self, index, ots_sig, auth_path):
        self.index = index
        self.ots_sig = ots_sig
        self.auth_path = auth_path


def lms_sign(message: bytes, keypair: LMSKeyPair) -> LMSSignature:
    for i in range(keypair.n):
        if i not in keypair.used:
            keypair.used.add(i)
            break
    else:
        raise Exception("No unused LMS keys left")

    # One-time signature (hash-based)
    ots_sig = H(keypair.private_keys[i] + message)

    auth_path = keypair.get_auth_path(i)
    return LMSSignature(i, ots_sig, auth_path)

# LM-OTS functions
#
def encode_lmots_sig(C, I, q, y):
    result = uint32ToString(lmots_sha256_n32_w8) + C + I + NULL + q
    for i, e in enumerate(y):
        result = result + y[i]
    return result

def decode_lmots_sig(sig):
    if (len(sig) != bytes_in_lmots_sig()):
        print("error decoding signature")
    typecode = sig[0:4]
    if (typecode != uint32ToString(lmots_sha256_n32_w8)):
        print("error decoding signature; got typecode " + stringToHex(typecode) + ", expected: " + stringToHex(uint32ToString(lmots_sha256_n32_w8)))
        return ""
    C = sig[4:n+4]
    I = sig[n+4:n+35]
    q = sig[n+36:n+40] # note: skip over NULL
    y = list()
    pos = n+40
    for i in range(0, p):
        y.append(sig[pos:pos+n])
        pos = pos + n
    return C, I, q, y

def print_lmots_sig(sig):
    C, I, q, y = decode_lmots_sig(sig)
    print( "C:\t" + stringToHex(C))
    print( "I:\t" + stringToHex(I))
    print( "q:\t" + stringToHex(q))
    for i, e in enumerate(y):
        print("y[" + str(i) + "]:\t" + stringToHex(e))

def lmots_gen_priv():
    priv = list()
    for i in range(0, p):
        priv.append(entropySource.read(n))
    return priv
def lmots_gen_pub(private_key, I, q):
    hash = SHA256.new()
    hash.update(I + q)
    for i, x in enumerate(private_key):
        tmp = x
        # print "i:" + str(i) + " range: " + str(range(0, 256))
        for j in range(0, 256):
            tmp = H(tmp + I + q + uint16ToString(i) + uint8ToString(j) + D_ITER)
        hash.update(tmp)
    hash.update(D_PBLC)
    return hash.digest()
def checksum(x):
    sum = 0
    for c in x:
        sum = sum + ord(c)
    # print format(sum, '04x')
    c1 = chr(sum >> 8)
    c2 = chr(sum & 0xff)
    return c1 + c2

def lmots_gen_sig(private_key, I, q, message):
    C = entropySource.read(n)
    hashQ = H(message + C + I + q + D_MESG)
    V = hashQ + checksum(hashQ)
    # print "V: " + stringToHex(V)
    y = list()
    for i, x in enumerate(private_key):
        tmp = x
        # print "i:" + str(i) + " range: " + str(range(0, ord(V[i])))
        for j in range(0, ord(V[i])):
            tmp = H(tmp + I + q + uint16ToString(i) + uint8ToString(j) + D_ITER)
        y.append(tmp)
    return encode_lmots_sig(C, I, q, y)

def lmots_sig_to_pub(sig, message):
    C, I, q, y = decode_lmots_sig(sig)
    hashQ = H(message + C + I + q + D_MESG)
    V = hashQ + checksum(hashQ)
    # print "V: " + stringToHex(V)
    hash = SHA256.new()
    hash.update(I + q)
    for i, y in enumerate(y):
        tmp = y
        # print "i:" + str(i) + " range: " + str(range(ord(V[i]), 256))
        for j in range(ord(V[i]), 256):
            tmp = H(tmp + I + q + uint16ToString(i) + uint8ToString(j) + D_ITER)
        hash.update(tmp)
    hash.update(D_PBLC)
    return hash.digest()

def lmots_verify_sig(public_key, sig, message):
    z = lmots_sig_to_pub(sig, message)
    # print "z: " + stringToHex(z)
    if z == public_key:
        return 1
    else:
        return 0
def LMS_test():
    print( "LMS test")
    print("Generating private keys now")
    lms_priv = lms_private_key()
    #print "Generated private keys"
    lms_pub = lms_public_key(lms_priv.get_public_key())
    #print "Generated public keys"
    sys.exit(1);

    # lms_priv.printHex()
    for i in range(0, 2**h):
        sig = lms_priv.sign(message)

        print("LMS signature byte length: " + str(len(sig)))

        # print_lms_sig(sig)

        #print "true positive test"
        if (lms_pub.verify(message, sig) == 1):
            print("passed: LMS message/signature pair is valid")
        else:
            print("failed: LMS message/signature pair is invalid")

        print("false positive test")
        if (lms_pub.verify("other message", sig) == 1):
            print("failed: LMS message/signature pair is valid (expected failure)")
        else:
            print("passed: LMS message/signature pair is invalid as expected")

def encode_hlms_sig(pub2, sig1, lms_sig):
    result = uint32ToString(hlms_sha256_n32_l2)
    result = result + pub2
    result = result + sig1
    result = result + lms_sig
    return result

def decode_hlms_sig(sig):
    typecode = sig[0:4]
    if (typecode != uint32ToString(hlms_sha256_n32_l2)):
        print("error decoding signature; got typecode " + stringToHex(typecode) + ", expected: " + stringToHex(uint32ToString(hlms_sha256_n32_l2)))
        return ""
    pub2 = sig[4:36]
    lms_sig_len = bytes_in_lms_sig()
    sig1 = sig[36:36+lms_sig_len]
    lms_sig = sig[36+lms_sig_len:36+2*lms_sig_len]
    return pub2, sig1, lms_sig

def print_hlms_sig(sig):
    pub2, sig1, lms_sig = decode_hlms_sig(sig)
    print("pub2:\t" + stringToHex(pub2))
    print("sig1: ")
    print_lms_sig(sig1)
    print("sig2: ")
    print_lms_sig(lms_sig)


        
#########################
def get_filetime(file):
    file_path = file
    stat = os.stat(file_path)

    #print("Accessed:", datetime.datetime.fromtimestamp(stat.st_atime))
    #print("Modified:", datetime.datetime.fromtimestamp(stat.st_mtime))
    #print("Created  :", datetime.datetime.fromtimestamp(stat.st_ctime))

    f1=datetime.datetime.fromtimestamp(stat.st_atime)
    f2=datetime.datetime.fromtimestamp(stat.st_mtime)
    f3=datetime.datetime.fromtimestamp(stat.st_ctime)
    ff1=str(f1)
    ff2=str(f2)
    ff3=str(f3)
    
    ft1=ff1.split(".")
    ftime1=ft1[0]
    ft2=ff2.split(".")
    ftime2=ft2[0]
    ft3=ff3.split(".")
    ftime3=ft3[0]
    file_info=[ftime1,ftime2,ftime3]
    return file_info
        
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    uname=""
    st=""
    data=[]
    drdata=[]
    fdata=[]
    s1=""
    s2=""
    fss=""
    sdata=[]
    vdata=[]
    listdrv=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    sys_drive=""

   
    driveStr = subprocess.check_output("fsutil fsinfo drives")
    drv=driveStr.decode(encoding='utf-8')
    drv1=drv.split('Drives: ')
    drv2=drv1[1].split(' ')
    dlen=len(drv2)
    i=0
    for rr in drv2:
        if i<dlen-1:
            drdata.append(rr)
        i+=1

    sys_drive=",".join(drdata)
    ff=open("static/drive_det.txt","w")
    ff.write(sys_drive)
    ff.close()

    if request.method=='POST':
        listdrv=request.form['listdrv']
        t1=request.form['t1']

        if listdrv=="":
            s=1
        else:
            s1="1"
            listdrv=request.form['listdrv']
            
            rootdir = listdrv
            
            for file in os.listdir(rootdir):
                
                d = os.path.join(rootdir, file)
                
                if os.path.isdir(d):
                    fb=os.path.basename(d)
                    if fb=="$RECYCLE.BIN" or fb=="Recovery" or fb=="System Volume Information":
                        s=1
                    else:
                        fd=[]
                        fd.append("dir")
                        fd.append(d)
                        print("dir="+d)
                        fdata.append(fd)

            for file in os.listdir(rootdir):
                
                d = os.path.join(rootdir, file)
                if os.path.isdir(d):
                    s=1
                else:
                    fb=os.path.basename(d)
                    if fb=="":
                        s=1
                    else:
                        fd1=[]
                        fd1.append("file")
                        fd1.append(d)
                        print("file="+d)
                        fdata.append(fd1)

        fn=request.form.getlist('c1[]')
        cnt=len(fn)
        hash1=""

        if t1=="1":
            s1="2"
        
        ###
        file_root=[]

        if t1=="2" and act is None:
            if cnt>0:
                
                for c11 in fn:
                    cf=c11.split("|")
                    if cf[0]=="dir":
                        for root, dirs, files in os.walk(cf[1]):
                
                            for file in files:
                                with open(os.path.join(root, file), "r") as auto:
                                    if file=="$RECYCLE.BIN" or file=="Recovery" or file=="System Volume Information":
                                        s=1
                                    else:
                                        fs=file.split(".")
                                        if len(fs)>0:
                                            froot=os.path.join(root, file)
                                            cfile=froot
                                            file_root.append(cfile)
                    else:
                        file_root.append(cf[1])
                        
            cnt2=len(file_root)
            if cnt2>0:
                
                #mycursor.execute("delete from tm_selected where status=0")
                #mydb.commit()
                for f_root in file_root:
                    
                    mycursor.execute("SELECT max(id)+1 FROM tm_selected")
                    maxid = mycursor.fetchone()[0]
                    if maxid is None:
                        maxid=1
                    
                    hash1 = calculate_hash(f_root)
                    
                    get_ft=get_filetime(f_root)
                    fnn=f_root+","
                    ff=open("static/bfile.txt","a")
                    ff.write(fnn)
                    ff.close()

                    mycursor.execute("SELECT count(*) FROM tm_selected where file_path=%s",(f_root,))
                    sn = mycursor.fetchone()[0]
                    if sn==0:
                        sql = "INSERT INTO tm_selected(id,uname,file_path,filetype,status,hash_val,atime,mtime,ctime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        val = (maxid,'admin',f_root,'file','0',hash1,get_ft[0],get_ft[1],get_ft[2])
                        mycursor.execute(sql, val)
                        mydb.commit()

                        bcdata="File ID:"+str(maxid)+","+f_root+", Created on "+get_ft[2]+", File Stored"
                        timechain(str(maxid),'admin',bcdata,'reg')
                    else:
                        mycursor.execute("update tm_selected set hash_val=%s,atime=%s,mtime=%s,ctime=%s where file_path=%s",(hash1,get_ft[0],get_ft[1],get_ft[2],f_root))
                        mydb.commit()
                        
                        bcdata="File ID:"+str(maxid)+","+f_root+", Created on "+get_ft[2]+", File Stored"
                        timechain(str(maxid),'admin',bcdata,'reg')
                 

    ##########
    if act=="clear":
        ff=open("static/key.txt","w")
        ff.write("1")
        ff.close()

        ff=open("static/bfile.txt","w")
        ff.write("")
        ff.close()

        ff=open("static/web/js/d1.txt","w")
        ff.write("")
        ff.close()

        mycursor.execute("delete from tm_selected")
        mydb.commit()
        return redirect(url_for('admin')) 

        
        

    mycursor.execute("SELECT count(*) FROM tm_selected")
    fcnt = mycursor.fetchone()[0]
    if fcnt>0:
        fss="1"
        mycursor.execute("SELECT * FROM tm_selected")
        sdata = mycursor.fetchall()

    '''for sd in sdata:
        fn=sd[2]
        print(fn)
        get_filetime(fn)
        print("**")
        fid=sd[0]
        bcdata="File ID:"+str(fid)+","+fn+""
        timechain(str(fid),'admin',bcdata,'reg')'''
  
    return render_template('web/admin.html',msg=msg,act=act,data=data,drdata=drdata,fdata=fdata,listdrv=listdrv,s1=s1,s2=s2,fss=fss,sdata=sdata)

def unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    #for x in unique_list:
    #    print x,
    return unique_list

@app.route('/page', methods=['GET', 'POST'])
def page():
    msg=""
    fss=""
    sdata=[]
    mess=""
    mess1=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tm_selected")
    sdata2 = mycursor.fetchall()

    mycursor.execute("SELECT * FROM tm_register where id=1")
    udata = mycursor.fetchone()
    name=udata[1]
    mobile=udata[2]
    email=udata[3]
    ##########
    print("bfile")
    ff=open("static/bfile.txt","r")
    file_r=ff.read()
    ff.close()
    sdd=file_r.split(",")
    slen=len(sdd)-1
    j=1
    for sdd1 in sdd:
       if j<=slen:
           print(sdd1)
           sdata.append(sdd1)
           j+=1
    print(sdata)
    print("----------")
    mycursor.execute("SELECT count(*) FROM tm_selected")
    fcnt = mycursor.fetchone()[0]
    if fcnt>0:
        fss="1"

        #####list the dir from other any new/relocate
        mycursor.execute("SELECT * FROM tm_selected")
        fd1 = mycursor.fetchall()
        filenames = []
        for fd11 in fd1:
            
            filename = os.path.basename(fd11[2])
            bpath=fd11[2]
            fd2=bpath.split(filename)
            fpath=fd2[0]
            
            directory = fpath
        
            for root, dirs, files in os.walk(directory):
                for file in files:
                    
                    ffile=os.path.join(root, file)
                    print(ffile)
                    #if fd11[2]==ffile:
                    #    print("sss")
                    mycursor.execute("SELECT count(*) FROM tm_selected where file_path=%s",(ffile,))
                    fc1 = mycursor.fetchone()[0]
                    if fc1==0:                        
                        filenames.append(ffile)

        filenames1=unique(filenames)

        #print(filenames1)
     
        for fname1 in filenames1:
            
            hash1 = calculate_hash(fname1)
            get_ft=get_filetime(fname1)
         
                
            mycursor.execute("SELECT count(*) FROM tm_selected where hash_val=%s",(hash1,))
            fcnt2 = mycursor.fetchone()[0]
            if fcnt2>0:
                mycursor.execute("SELECT max(id)+1 FROM tm_selected")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1

                sql = "INSERT INTO tm_selected(id,uname,file_path,filetype,status,hash_val,atime,mtime,ctime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,'admin',fname1,'file','0',hash1,get_ft[0],get_ft[1],get_ft[2])
                mycursor.execute(sql, val)
                mydb.commit()
                mess="Dear "+name+",FileID:"+str(maxid)+", File Moved"
                bcdata="File ID:"+str(maxid)+","+fname1+", on "+get_ft[2]+", File Moved to other Location"
                timechain(str(maxid),'admin',bcdata,'reg')

            else:
                mycursor.execute("SELECT max(id)+1 FROM tm_selected")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1

                
                sql = "INSERT INTO tm_selected(id,uname,file_path,filetype,status,hash_val,atime,mtime,ctime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (maxid,'admin',fname1,'file','0',hash1,get_ft[0],get_ft[1],get_ft[2])
                mycursor.execute(sql, val)
                mydb.commit()

                bcdata="File ID:"+str(maxid)+","+fname1+", Created on "+get_ft[2]+", File Stored"
                timechain(str(maxid),'admin',bcdata,'reg')
                
            bf_data=""
            bfd=[]
            mycursor.execute("SELECT * FROM tm_selected")
            fd3 = mycursor.fetchall()
            for fd4 in fd3:
                bfd.append(fd4[2])
            bf_data=",".join(bfd)
            bf_data1=bf_data+","
            ff=open("static/bfile.txt","w")
            ff.write(bf_data1)
            ff.close()
        

        
        
        for sd1 in sdata:
            
            mycursor.execute("SELECT count(*) FROM tm_selected where file_path=%s",(sd1,))
            sn = mycursor.fetchone()[0]
            if sn>0:
                mycursor.execute("SELECT * FROM tm_selected where file_path=%s",(sd1,))
                sd = mycursor.fetchone()
                fn=sd[2]
                
                fid=sd[0]

                at=0
                mt=0
                ct=0
                if os.path.isfile(fn):
                    get_ft=get_filetime(fn)
                    atime=get_ft[0]
                    mtime=get_ft[1]
                    ctime=get_ft[2]
                    mycursor.execute("update tm_selected set dstatus=0,mstatus=0 where file_path=%s",(sd1,))
                    mydb.commit()
                    
                    ####
                    if sd[8]==atime:
                        s=1
                    else:
                        at+=1

                    if at>0:
                        if atime==sd[11]:
                            s=1
                        else:
                            mycursor.execute("update tm_selected set atime2=%s where file_path=%s",(atime,sd1))
                            mydb.commit()

                            mess="Dear "+name+",FileID:"+str(fid)+", File Accessed"
                            
                            bcdata="File ID:"+str(fid)+","+fn+", Access on "+get_ft[0]+", File Accessed"
                            timechain(str(fid),'admin',bcdata,'reg')
                    ####
                    if sd[9]==mtime:
                        s=1
                    else:
                        mt+=1
                    if mt>0:
                        if mtime==sd[12]:
                            s=1
                        else:
                            mycursor.execute("update tm_selected set mtime2=%s where file_path=%s",(mtime,sd1))
                            mydb.commit()

                            mess="Dear "+name+",FileID:"+str(fid)+", File Modified"
                            mess1="FileID:"+str(fid)+", File Modified"
                            bcdata="File ID:"+str(fid)+","+fn+", Modify on "+get_ft[1]+", File Modified"
                            timechain(str(fid),'admin',bcdata,'reg')

                    ####
                    if sd[10]==ctime:
                        s=1
                    else:
                        ct+=1
                    if ct>0:
                        if ctime==sd[13]:
                            s=1
                        else:
                            mycursor.execute("update tm_selected set ctime2=%s where file_path=%s",(ctime,sd1))
                            mydb.commit()

                            mess="Dear "+name+",FileID:"+str(fid)+", File Created Time Changed"
                            mess1="FileID:"+str(fid)+", File Created Time Changed"
                            bcdata="File ID:"+str(fid)+","+fn+", Changed Time:"+get_ft[1]+", File Created Time Changed"
                            timechain(str(fid),'admin',bcdata,'reg')
                        
                else:
                    s=1
                    fcount=0
                    ##Change location
                    
                    ##delete
                    if sd[14]==0 and fcount==0:
                        mycursor.execute("update tm_selected set dstatus=1 where file_path=%s",(sd1,))
                        mydb.commit()
                            
                        fst=fn.split(".")
                        ext=fst[1]

                        mess="Dear "+name+",FileID:"+str(fid)+", File Deleted"
                        mess1="FileID:"+str(fid)+", File Deleted"
                        bcdata="File ID:"+str(fid)+","+fn+", File Deleted"
                        timechain(str(fid),'admin',bcdata,'reg')
                

    return render_template('web/page.html',msg=msg,fss=fss,sdata=sdata,sdata2=sdata2,mess=mess,mess1=mess1,email=email,name=name,mobile=mobile)

def change_creation_time(file_path, new_time):
    # Open the file with GENERIC_WRITE access
    handle = win32file.CreateFile(
        file_path,
        win32con.GENERIC_WRITE,
        0,
        None,
        win32con.OPEN_EXISTING,
        0,
        None
    )

    # Convert datetime to Windows file time
    win_time = pywintypes.Time(new_time)

    # Set file times: (creation, access, modification)
    win32file.SetFileTime(handle, win_time, None, None)

    handle.close()
@app.route('/attack', methods=['GET', 'POST'])
def attack():
    msg=""
    if request.method == 'POST':
        file_path = request.form['file_path']
        change_time = request.form['change_time']
        #change_creation_time(file_path, change_time)
        #print("Creation time changed successfully.")
        
        #####
        original_file = file_path
        copy_location = file_path
        fake_timestamp = change_time  
        spoof_time = time.mktime(time.strptime(fake_timestamp, "%Y-%m-%d %H:%M:%S"))
        os.utime(copy_location, (spoof_time, spoof_time))
        print(f"[+] Modified access & modified times set to {fake_timestamp}")

        # --- Step 3: Set creation time (Windows only) ---
        if platform.system() == "Windows":
            try:
                import pywintypes
                import win32file
                import win32con

                handle = win32file.CreateFile(
                    copy_location, win32con.GENERIC_WRITE, 0, None,
                    win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None
                )
                new_ctime = pywintypes.Time(datetime.datetime.strptime(fake_timestamp, "%Y-%m-%d %H:%M:%S"))
                win32file.SetFileTime(handle, new_ctime, None, None)
                handle.close()
                print(f"[+] Created time spoofed (Windows only)")
            except ImportError:
                print("[!] pywin32 not installed. Creation time not spoofed.")
        else:
            print("[*] Skipping creation time (not supported on this OS)")

        # --- Step 4: Show Result ---
        stat = os.stat(copy_location)
        print("\n[+] Final timestamps:")
        print("    Accessed :", datetime.datetime.fromtimestamp(stat.st_atime))
        print("    Modified :", datetime.datetime.fromtimestamp(stat.st_mtime))
        print("    Created  :", datetime.datetime.fromtimestamp(stat.st_ctime))
        msg="ok"
    return render_template('web1/attack.html',msg=msg)

@app.route('/view_block', methods=['GET', 'POST'])
def view_block():
    msg=""
    cnt=0
    uname=""
    data1=[]
    mess=""
    act=request.args.get("act")

    if act=="1":
        ff=open("static/timechain.json","r")
        fj=ff.read()
        ff.close()

        fjj=fj.split('}')

        nn=len(fjj)
        nn2=nn-2
        i=0
        fsn=""
        while i<nn-1:
            if i==nn2:
                fsn+=fjj[i]+"}"
            else:
                fsn+=fjj[i]+"},"
            i+=1
            
        #fjj1='},'.join(fjj)
        
        fj1="["+fsn+"]"
        

       

    ################
    
    if act=="11":
        if request.method=='POST':
            fid=request.form['fid']
            fname=request.form['fname']

            s1="1"
            ff=open("static/web/js/d1.txt","r")
            ds=ff.read()
            ff.close()

            drow=ds.split("#|")
            
            i=0
            for dr in drow:
                
                dr1=dr.split("##")
                dt=[]

                sd1=dr1[2].split(',')
                sd2=sd1[0].split(":")
                
                

                if sd2[1]==fid or fname in sd1[1]:
                    dt.append(dr1[0])
                    dt.append(dr1[1])
                    dt.append(dr1[2])
                    dt.append(dr1[3])
                    #dt.append(dr1[4])
                    if "File Modified" in dr1[2] or "File Deleted" in dr1[2] or "File Moved" in dr1[2] or "File Created" in dr1[2]:
                        dt.append("2")
                    elif "File Accessed" in dr1[2]:
                        dt.append("3")
                    else:
                        dt.append("1")
                    data1.append(dt)

        else:
            s1="1"
            ff=open("static/web/js/d1.txt","r")
            ds=ff.read()
            ff.close()

            drow=ds.split("#|")
            
            i=0
            for dr in drow:
                
                dr1=dr.split("##")
                dt=[]
                #if "Register" in dr1[2]:
                
                    
                    
                dt.append(dr1[0])
                dt.append(dr1[1])
                dt.append(dr1[2])
                dt.append(dr1[3])
                #dt.append(dr1[4])
                if "File Modified" in dr1[2] or "File Deleted" in dr1[2] or "File Moved" in dr1[2] or "File Created" in dr1[2]:
                    dt.append("2")
                elif "File Accessed" in dr1[2]:
                    dt.append("3")
                else:
                    dt.append("1")
                data1.append(dt)
    else:
        ff=open("static/web/js/d1.txt","r")
        ds=ff.read()
        ff.close()

        drow=ds.split("#|")
        
        i=0
        for dr in drow:
            
            dr1=dr.split("##")
            dt=[]
            #if "Register" in dr1[2]:
                
            dt.append(dr1[0])
            dt.append(dr1[1])
            dt.append(dr1[2])
            dt.append(dr1[3])
            #dt.append(dr1[4])
            data1.append(dt)
        
    
    return render_template('web/view_block.html',msg=msg,act=act,data1=data1)


@app.route('/down', methods=['GET', 'POST'])
def down():
    fn = request.args.get('fname')
    path = request.args.get('path')
    pp=path.split("\\")
    print(pp)
    fv=""
    if len(pp)>0:
        for p1 in pp:
            fv+=p1+"/"

    print(fv)
    print(fn)
    path1=fv+fn
    
    return send_file(path1, as_attachment=True)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
