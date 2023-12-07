def p1():
    return """#include<stdio.h>

int main() {
    char message[100], ch;
    int i, key;
    
    printf("Enter a message to encrypt: ");
    gets(message);
    
    printf("Enter key: ");
    scanf("%d", &key);
    
    for(i = 0; message[i] != '\0'; ++i) {
        ch = message[i];
        
        if(ch >= 'a' && ch <= 'z') {
            ch = ch + key;
            
            if(ch > 'z') {
                ch = ch - 'z' + 'a' - 1;
            }
            
            message[i] = ch;
        } 
        else if(ch >= 'A' && ch <= 'Z') {
            ch = ch + key;
            
            if(ch > 'Z') {
                ch = ch - 'Z' + 'A' - 1;
            }
            
            message[i] = ch;
        }
    }
    
    printf("Encrypted message: %s", message);
    
    return 0;
}

"""

def p2():
    return """#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define SIZE 30

// Function to convert the string to lowercase
void toLowerCase(char plain[], int ps) {
    int i;
    for (i = 0; i < ps; i++) {
        if (plain[i] > 64 && plain[i] < 91)
            plain[i] += 32;
    }
}

// Function to remove all spaces in a string
int removeSpaces(char* plain, int ps) {
    int i, count = 0;
    for (i = 0; i < ps; i++)
        if (plain[i] != ' ')
            plain[count++] = plain[i];
    plain[count] = '\0';
    return count;
}

// Function to generate the 5x5 key square
void generateKeyTable(char key[], int ks, char keyT[5][5]) {
    int i, j, k, flag = 0, *dicty;

    // a 26 character hashmap
    // to store count of the alphabet
    dicty = (int*)calloc(26, sizeof(int));

    for (i = 0; i < ks; i++) {
        if (key[i] != 'j')
            dicty[key[i] - 97] = 2;
    }

    dicty['j' - 97] = 1;
    i = 0;
    j = 0;

    for (k = 0; k < ks; k++) {
        if (dicty[key[k] - 97] == 2) {
            dicty[key[k] - 97] -= 1;
            keyT[i][j] = key[k];
            j++;

            if (j == 5) {
                i++;
                j = 0;
            }
        }
    }

    for (k = 0; k < 26; k++) {
        if (dicty[k] == 0) {
            keyT[i][j] = (char)(k + 97);
            j++;

            if (j == 5) {
                i++;
                j = 0;
            }
        }
    }
}

// Function to search for the characters of a digraph
// in the key square and return their position
void search(char keyT[5][5], char a, char b, int arr[]) {
    int i, j;

    if (a == 'j')
        a = 'i';
    else if (b == 'j')
        b = 'i';

    for (i = 0; i < 5; i++) {
        for (j = 0; j < 5; j++) {
            if (keyT[i][j] == a) {
                arr[0] = i;
                arr[1] = j;
            } else if (keyT[i][j] == b) {
                arr[2] = i;
                arr[3] = j;
            }
        }
    }
}

// Function to find the modulus with 5
int mod5(int a) {
    return (a % 5);
}

// Function to make the plain text length to be even
int prepare(char str[], int ptrs) {
    if (ptrs % 2 != 0) {
        str[ptrs++] = 'z';
        str[ptrs] = '\0';
    }
    return ptrs;
}

// Function for performing the encryption
void encrypt(char str[], char keyT[5][5], int ps) {
    int i, a[4];

    for (i = 0; i < ps; i += 2) {
        search(keyT, str[i], str[i + 1], a);

        if (a[0] == a[2]) {
            str[i] = keyT[a[0]][mod5(a[1] + 1)];
            str[i + 1] = keyT[a[0]][mod5(a[3] + 1)];
        } else if (a[1] == a[3]) {
            str[i] = keyT[mod5(a[0] + 1)][a[1]];
            str[i + 1] = keyT[mod5(a[2] + 1)][a[1]];
        } else {
            str[i] = keyT[a[0]][a[3]];
            str[i + 1] = keyT[a[2]][a[1]];
        }
    }
}

// Function to encrypt using Playfair Cipher
void encryptByPlayfairCipher(char str[], char key[]) {
    char ps, ks, keyT[5][5];

    // Key
    ks = strlen(key);
    ks = removeSpaces(key, ks);
    toLowerCase(key, ks);

    // Plaintext
    ps = strlen(str);
    toLowerCase(str, ps);
    ps = removeSpaces(str, ps);
    ps = prepare(str, ps);

    generateKeyTable(key, ks, keyT);
    encrypt(str, keyT, ps);
}

// Driver code
int main() {
    char str[SIZE], key[SIZE];

    // Key to be encrypted
    strcpy(key, "Monarchy");
    printf("Key text: %s\n", key);

    // Plaintext to be encrypted
    strcpy(str, "instruments");
    printf("Plain text: %s\n", str);

    // encrypt using Playfair Cipher
    encryptByPlayfairCipher(str, key);
    printf("Cipher text: %s\n", str);

    return 0;
}

"""

def p3():
    return """#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int **matrixmultiply(int **a, int r1, int c1, int **b, int r2, int c2) {
    int **resultmatrix;
    int i, j, k, r, c;
    r = r1;
    c = c2;
    
    resultmatrix = (int**)malloc(sizeof(int*) * r);
    for (i = 0; i < r; i++)
        resultmatrix[i] = (int*)malloc(sizeof(int) * c);

    for (i = 0; i < r; i++) {
        for (j = 0; j < c; j++) {
            resultmatrix[i][j] = 0;
            for (k = 0; k < c1; k++)
                resultmatrix[i][j] += a[i][k] * b[k][j];
        }
    }

    return resultmatrix;
}

void printmatrix(int** matrix, int r, int c) {
    int i, j;
    for (i = 0; i < r; i++) {
        for (j = 0; j < c; j++)
            printf("%d", matrix[i][j]);
        printf("\n");
    }
}

int plaintexttociphertext(char plaintext[], int** matrix) {
    int len, **plaintextmatrix, **resultmatrix, i, j;
    
    // the matrix will be of dimensions strlen(plain text) by strlen(plain text)
    char *ciphertext;
    len = strlen(plaintext);
    ciphertext = (char*)malloc(sizeof(char) * 1000);

    // plaintextmatrix should be of dimension strlen(plain text) by 1
    // allocating memory to plaintextmatrix
    plaintextmatrix = (int**)malloc(sizeof(int*) * len);
    for (i = 0; i < len; i++)
        plaintextmatrix[i] = (int*)malloc(sizeof(int) * 1);

    // populating the plaintextmatrix
    for (i = 0; i < len; i++)
        for (j = 0; j < 1; j++)
            plaintextmatrix[i][j] = plaintext[i] - 'a';

    resultmatrix = matrixmultiply(matrix, len, len, plaintextmatrix, len, 1);

    // taking mod26 of each element of result matrix
    for (i = 0; i < len; i++)
        for (j = 0; j < 1; j++)
            resultmatrix[i][j] %= 26;

    // printing the cipher text
    printf("The cipher text is as follows:");
    for (i = 0; i < len; i++)
        for (j = 0; j < 1; j++)
            printf("%c", resultmatrix[i][j] + 'a');
    printf("\n");
}

int main() {
    int len, i, j, **matrix;
    char plaintext[1000];

    printf("Enter the word to be encrypted:");
    scanf("%s", plaintext);
    len = strlen(plaintext);

    // allocating memory to matrix
    matrix = (int**)malloc(sizeof(int*) * len);
    for (i = 0; i < len; i++)
        matrix[i] = (int*)malloc(sizeof(int) * len);

    printf("Enter matrix of %d by %d to be used in encryption process:\n", len, len);
    for (i = 0; i < len; i++)
        for (j = 0; j < len; j++)
            scanf("%d", &matrix[i][j]);

    plaintexttociphertext(plaintext, matrix);

    return 0;
}

"""

def p4():
    return """#include<stdio.h>
#include<string.h>

int main() {
    char msg[] = "THECRAZYPROGRAMMER";
    char key[] = "HELLO";
    int msgLen = strlen(msg), keyLen = strlen(key), i, j;
    char newKey[msgLen], encryptedMsg[msgLen], decryptedMsg[msgLen];

    // generating new key
    for (i = 0, j = 0; i < msgLen; ++i, ++j) {
        if (j == keyLen)
            j = 0;
        newKey[i] = key[j];
    }
    newKey[i] = '\0';

    // encryption
    for (i = 0; i < msgLen; ++i)
        encryptedMsg[i] = ((msg[i] + newKey[i]) % 26) + 'A';
    encryptedMsg[i] = '\0';

    // decryption
    for (i = 0; i < msgLen; ++i)
        decryptedMsg[i] = (((encryptedMsg[i] - newKey[i]) + 26) % 26) + 'A';
    decryptedMsg[i] = '\0';

    printf("Original Message: %s", msg);
    printf("\nKey: %s", key);
    printf("\nNew Generated Key: %s", newKey);
    printf("\nEncrypted Message: %s", encryptedMsg);
    printf("\nDecrypted Message: %s", decryptedMsg);

    return 0;
}

"""

def p5():
    return """#include<stdio.h>
#include<string.h>
#include<stdlib.h>

int main() {
    int i, j, len, rails, count, code[100][1000];
    char str[1000];
    
    printf("Enter a Secret Message\n");
    gets(str);
    len = strlen(str);
    
    printf("Enter number of rails\n");
    scanf("%d", &rails);
    
    for (i = 0; i < rails; i++) {
        for (j = 0; j < len; j++) {
            code[i][j] = 0;
        }
    }
    
    count = 0;
    j = 0;
    
    while (j < len) {
        if (count % 2 == 0) {
            for (i = 0; i < rails; i++) {
                code[i][j] = (int)str[j];
                j++;
            }
        } else {
            for (i = rails - 2; i > 0; i--) {
                code[i][j] = (int)str[j];
                j++;
            }
        }
        count++;
    }
    
    for (i = 0; i < rails; i++) {
        for (j = 0; j < len; j++) {
            if (code[i][j] != 0)
                printf("%c", code[i][j]);
        }
    }
    
    printf("\n");

    return 0;
}

"""

def p6():
    return """import javax.swing.*;
import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.util.Random;

class Des {
    byte[] skey = new byte[1000];
    String skeyString;
    static byte[] raw;
    String inputMessage, encryptedData, decryptedMessage;

    public Des() {
        try {
            generateSymmetricKey();
            inputMessage = JOptionPane.showInputDialog(null, "Enter message to encrypt");
            byte[] ibyte = inputMessage.getBytes();
            byte[] ebyte = encrypt(raw, ibyte);
            encryptedData = new String(ebyte);
            System.out.println("Encrypted message " + encryptedData);
            JOptionPane.showMessageDialog(null, "Encrypted Data" + "\n" + encryptedData);
            byte[] dbyte = decrypt(raw, ebyte);
            decryptedMessage = new String(dbyte);
            System.out.println("Decrypted message" + decryptedMessage);
            JOptionPane.showMessageDialog(null, "Decrypted Data" + "\n" + decryptedMessage);
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    void generateSymmetricKey() {
        try {
            Random r = new Random();
            int num = r.nextInt(10000);
            String knum = String.valueOf(num);
            byte[] knumb = knum.getBytes();
            skey = getRawKey(knumb);
            skeyString = new String(skey);
            System.out.println("DES Symmetric key = " + skeyString);
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    private static byte[] getRawKey(byte[] seed) throws Exception {
        KeyGenerator kgen = KeyGenerator.getInstance("DES");
        SecureRandom sr = SecureRandom.getInstance("SHA1PRNG");
        sr.setSeed(seed);
        kgen.init(56, sr);
        SecretKey skey = kgen.generateKey();
        raw = skey.getEncoded();
        return raw;
    }

    private static byte[] encrypt(byte[] raw, byte[] clear) throws Exception {
        SecretKeySpec skeySpec = new SecretKeySpec(raw, "DES");
        Cipher cipher = Cipher.getInstance("DES");
        cipher.init(Cipher.ENCRYPT_MODE, skeySpec);
        byte[] encrypted = cipher.doFinal(clear);
        return encrypted;
    }

    private static byte[] decrypt(byte[] raw, byte[] encrypted) throws Exception {
        SecretKeySpec skeySpec = new SecretKeySpec(raw, "DES");
        Cipher cipher = Cipher.getInstance("DES");
        cipher.init(Cipher.DECRYPT_MODE, skeySpec);
        byte[] decrypted = cipher.doFinal(encrypted);
        return decrypted;
    }

    public static void main(String args[]) {
        Des des = new Des();
    }
}

"""

def p7():
    return """import java.security.*;

class JceSha1Test {
    public static void main(String[] a) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA1");
            System.out.println("Message digest object info: ");
            System.out.println(" Algorithm = " + md.getAlgorithm());
            System.out.println(" Provider = " + md.getProvider());
            System.out.println(" toString = " + md.toString());
            
            String input = "";
            md.update(input.getBytes());
            byte[] output = md.digest();
            
            System.out.println();
            System.out.println("SHA1(\"" + input + "\") =");
            System.out.println(" " + bytesToHex(output));

            input = "abc";
            md.update(input.getBytes());
            output = md.digest();
            
            System.out.println();
            System.out.println("SHA1(\"" + input + "\") =");
            System.out.println(" " + bytesToHex(output));

            input = "abcdefghijklmnopqrstuvwxyz";
            md.update(input.getBytes());
            output = md.digest();
            
            System.out.println();
            System.out.println("SHA1(\"" + input + "\") =");
            System.out.println(" " + bytesToHex(output));

        } catch (Exception e) {
            System.out.println("Exception: " + e);
        }
    }

    public static String bytesToHex(byte[] b) {
        char hexDigit[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
        StringBuffer buf = new StringBuffer();
        
        for (int j = 0; j < b.length; j++) {
            buf.append(hexDigit[(b[j] >> 4) & 0x0f]);
            buf.append(hexDigit[b[j] & 0x0f]);
        }
        
        return buf.toString();
    }
}

"""

def p8():
    return """// import statements
import java.math.BigInteger;
import java.security.NoSuchAlgorithmException;
import java.security.MessageDigest;

// A Java program that uses the MD5 to do the hashing
public class MD5 {
    public static String getMd5(String input) {
        try {
            // invoking the static getInstance() method of the MessageDigest class
            // Notice it has MD5 in its parameter.
            MessageDigest msgDst = MessageDigest.getInstance("MD5");

            // the digest() method is invoked to compute the message digest
            // from an input digest() and it returns an array of byte
            byte[] msgArr = msgDst.digest(input.getBytes());

            // getting signum representation from byte array msgArr
            BigInteger bi = new BigInteger(1, msgArr);

            // Converting into hex value
            String hshtxt = bi.toString(16);

            while (hshtxt.length() < 32) {
                hshtxt = "0" + hshtxt;
            }
            return hshtxt;
        }
        // for handling the exception
        catch (NoSuchAlgorithmException abc) {
            throw new RuntimeException(abc);
        }
    }

    // main method code
    public static void main(String argvs[]) throws NoSuchAlgorithmException {
        String str = "ssitise";
        String hash = getMd5(str);
        str = "'isedept'";
        System.out.println("The HashCode Generated for " + str + " is: " + hash);
    }
}

"""

def p9():
    return """import java.util.*;
import java.math.BigInteger;

class DSAAlgorithm {
    final static BigInteger one = new BigInteger("1");
    final static BigInteger zero = new BigInteger("0");

    public static BigInteger getNextPrime(String ans) {
        BigInteger test = new BigInteger(ans);
        while (!test.isProbablePrime(99)) {
            test = test.add(one);
        }
        return test;
    }

    public static BigInteger findQ(BigInteger n) {
        BigInteger start = new BigInteger("2");
        while (!n.isProbablePrime(99)) {
            while (!((n.mod(start)).equals(zero))) {
                start = start.add(one);
            }
            n = n.divide(start);
        }
        return n;
    }

    public static BigInteger getGen(BigInteger p, BigInteger q, Random r) {
        BigInteger h = new BigInteger(p.bitLength(), r);
        h = h.mod(p);
        return h.modPow((p.subtract(one)).divide(q), p);
    }

    public static void main(String[] args) throws java.lang.Exception {
        Random randObj = new Random();
        BigInteger p = getNextPrime("10600"); /* approximate prime */
        BigInteger q = findQ(p.subtract(one));
        BigInteger g = getGen(p, q, randObj);

        System.out.println("\nSimulation of Digital Signature Algorithm\n");
        System.out.println("\nGlobal public key components are:\n");
        System.out.println("\np is: " + p);
        System.out.println("\nq is: " + q);
        System.out.println("\ng is: " + g);

        BigInteger x = new BigInteger(q.bitLength(), randObj);
        x = x.mod(q);
        BigInteger y = g.modPow(x, p);
        BigInteger k = new BigInteger(q.bitLength(), randObj);
        k = k.mod(q);
        BigInteger r = (g.modPow(k, p)).mod(q);
        BigInteger hashVal = new BigInteger(p.bitLength(), randObj);
        BigInteger kInv = k.modInverse(q);
        BigInteger s = kInv.multiply(hashVal.add(x.multiply(r)));
        s = s.mod(q);

        System.out.println("\nSecret information are:\n");
        System.out.println("x (private) is:" + x);
        System.out.println("k (secret) is: " + k);
        System.out.println("y (public) is: " + y);
        System.out.println("h (rndhash) is: " + hashVal);

        System.out.println("\nGenerating digital signature:\n");
        System.out.println("r is : " + r);
        System.out.println("s is : " + s);

        BigInteger w = s.modInverse(q);
        BigInteger u1 = (hashVal.multiply(w)).mod(q);
        BigInteger u2 = (r.multiply(w)).mod(q);
        BigInteger v = (g.modPow(u1, p)).multiply(y.modPow(u2, p));
        v = (v.mod(p)).mod(q);

        System.out.println("\nVerifying digital signature (checkpoints)\n:");
        System.out.println("w is : " + w);
        System.out.println("u1 is : " + u1);
        System.out.println("u2 is : " + u2);
        System.out.println("v is : " + v);

        if (v.equals(r)) {
            System.out.println("\nSuccess: Digital signature is verified!\n " + r);
        } else {
            System.out.println("\nError: Incorrect digital signature\n");
        }
    }
}

"""

def p10a():
    return """#include <stdio.h>
#include <stdlib.h>
#define ll long long

/*
 * Modular exponentiation
 */
ll modulo(ll base, ll exponent, ll mod) {
    ll x = 1;
    ll y = base;

    while (exponent > 0) {
        if (exponent % 2 == 1)
            x = (x * y) % mod;
        y = (y * y) % mod;
        exponent = exponent / 2;
    }

    return x % mod;
}

/*
 * Fermat's test for checking primality
 */
int Fermat(ll p, int iterations) {
    int i;

    if (p == 1) {
        return 0;
    }

    for (i = 0; i < iterations; i++) {
        ll a = rand() % (p - 1) + 1;
        if (modulo(a, p - 1, p) != 1) {
            return 0;
        }
    }

    return 1;
}

/*
 * Main
 */
int main() {
    int iteration = 50;
    ll num;

    printf("Enter integer to test primality: ");
    scanf("%lld", &num);

    if (Fermat(num, iteration) == 1)
        printf("%lld is prime ", num);
    else
        printf("%lld is not prime ", num);

    return 0;
}

"""

def p10b():
    return """#include <stdio.h>

// Function to return gcd of a and b
int gcd(int a, int b) {
    if (a == 0)
        return b;
    return gcd(b % a, a);
}

// A simple method to evaluate Euler Totient Function
int phi(unsigned int n) {
    unsigned int result = 1;

    for (int i = 2; i < n; i++)
        if (gcd(i, n) == 1)
            result++;

    return result;
}

// Driver program to test above function
int main() {
    int n;

    for (n = 1; n <= 10; n++)
        printf("phi(%d) = %d\n", n, phi(n));

    return 0;
}

"""

def p11():
    return """// Java program to demonstrate the creation
// of Encryption and Decryption with Java AES
import java.nio.charset.StandardCharsets;
import java.security.spec.KeySpec;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

class AES {
    // Class private variables
    private static final String SECRET_KEY = "my_super_secret_key_ho_ho_ho";
    private static final String SALT = "ssshhhhhhhhhhh!!!!";

    // This method is used to encrypt a string
    public static String encrypt(String strToEncrypt) {
        try {
            // Create default byte array
            byte[] iv = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
            IvParameterSpec ivspec = new IvParameterSpec(iv);

            // Create SecretKeyFactory object
            SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");

            // Create KeySpec object and assign with constructor
            KeySpec spec = new PBEKeySpec(SECRET_KEY.toCharArray(), SALT.getBytes(), 65536, 256);
            SecretKey tmp = factory.generateSecret(spec);
            SecretKeySpec secretKey = new SecretKeySpec(tmp.getEncoded(), "AES");

            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            cipher.init(Cipher.ENCRYPT_MODE, secretKey, ivspec);

            // Return encrypted string
            return Base64.getEncoder().encodeToString(cipher.doFinal(strToEncrypt.getBytes(StandardCharsets.UTF_8)));
        } catch (Exception e) {
            System.out.println("Error while encrypting: " + e.toString());
        }
        return null;
    }

    // This method is used to decrypt a string
    public static String decrypt(String strToDecrypt) {
        try {
            // Default byte array
            byte[] iv = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

            // Create IvParameterSpec object and assign with constructor
            IvParameterSpec ivspec = new IvParameterSpec(iv);

            // Create SecretKeyFactory Object
            SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");

            // Create KeySpec object and assign with constructor
            KeySpec spec = new PBEKeySpec(SECRET_KEY.toCharArray(), SALT.getBytes(), 65536, 256);
            SecretKey tmp = factory.generateSecret(spec);
            SecretKeySpec secretKey = new SecretKeySpec(tmp.getEncoded(), "AES");

            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5PADDING");
            cipher.init(Cipher.DECRYPT_MODE, secretKey, ivspec);

            // Return decrypted string
            return new String(cipher.doFinal(Base64.getDecoder().decode(strToDecrypt)));
        } catch (Exception e) {
            System.out.println("Error while decrypting: " + e.toString());
        }
        return null;
    }
}

// Driver code
public class Main {
    public static void main(String[] args) {
        // Create String variables
        String originalString = "SSIT ISE";

        // Call encryption method
        String encryptedString = AES.encrypt(originalString);

        // Call decryption method
        String decryptedString = AES.decrypt(encryptedString);

        // Print all strings
        System.out.println(originalString);
        System.out.println(encryptedString);
        System.out.println(decryptedString);
    }
}

"""
