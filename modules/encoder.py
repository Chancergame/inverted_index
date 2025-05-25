import numpy as np

class NoneEncoder:
    @staticmethod
    def encode(data):
        return data
    
    @staticmethod
    def decode(data):
        return data

class GammaEncoder:
    @staticmethod
    def encode(data):
        sorted_data = sorted(data)
        bits = []
        for n in sorted_data:
            if n < 1:
                raise ValueError("Gamma encoding supports positive integers only")
            bin_n = bin(n)[2:]
            length = len(bin_n) - 1
            unary = '0' * length + '1'
            remainder = bin_n[1:] if length > 0 else ''
            bits.append(unary + remainder)
        bit_str = ''.join(bits)
        byte_arr = bytearray()
        for i in range(0, len(bit_str), 8):
            chunk = bit_str[i:i+8].ljust(8, '0')
            byte_arr.append(int(chunk, 2))
        return bytes(byte_arr)
    
    @staticmethod
    def decode(encoded_bytes):
        bit_str = ''.join(f"{byte:08b}" for byte in encoded_bytes)
        bits_iter = iter(bit_str)
        numbers = []
        while True:
            try:
                length = 0
                bit = next(bits_iter)
                while bit != '1':
                    length += 1
                    bit = next(bits_iter)
                remainder = []
                for _ in range(length):
                    remainder.append(next(bits_iter))
                if length == 0:
                    num = 1
                else:
                    num = int('1' + ''.join(remainder), 2)
                numbers.append(num)
            except StopIteration:
                break
        return set(numbers)

class DeltaEncoder:
    @staticmethod
    def encode(data):
        sorted_data = sorted(data)
        bits = []
        for n in sorted_data:
            if n < 1:
                raise ValueError("Delta encoding supports positive integers only")
            bin_n = bin(n)[2:]
            m = len(bin_n)
            bin_m = bin(m)[2:]
            gamma_length = len(bin_m) - 1
            gamma_unary = '0' * gamma_length + '1'
            gamma_remainder = bin_m[1:] if gamma_length > 0 else ''
            delta_remainder = bin_n[1:] if m > 1 else ''
            bits.append(gamma_unary + gamma_remainder + delta_remainder)
        bit_str = ''.join(bits)
        byte_arr = bytearray()
        for i in range(0, len(bit_str), 8):
            chunk = bit_str[i:i+8].ljust(8, '0')
            byte_arr.append(int(chunk, 2))
        return bytes(byte_arr)
    
    @staticmethod
    def decode(encoded_bytes):
        bit_str = ''.join(f"{byte:08b}" for byte in encoded_bytes)
        bits_iter = iter(bit_str)
        numbers = []
        while True:
            try:
                m_length = 0
                bit = next(bits_iter)
                while bit != '1':
                    m_length += 1
                    bit = next(bits_iter)
                m_remainder = []
                for _ in range(m_length):
                    m_remainder.append(next(bits_iter))
                if m_length == 0:
                    m = 1
                else:
                    m = int('1' + ''.join(m_remainder), 2)
                delta_remainder = []
                for _ in range(m - 1):
                    delta_remainder.append(next(bits_iter))
                num = int('1' + ''.join(delta_remainder), 2) if delta_remainder else 1
                numbers.append(num)
            except StopIteration:
                break
        return set(numbers)
        