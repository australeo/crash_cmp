#include <iostream>
#include <string>
#include <fstream>

void error(const std::string& e) {
    std::cout << e << std::endl;
}

typedef void fake_function(int);

unsigned long buf = 0xcafebabe;

void crash_one(int a) {
    *(int*)0xdeadbeef = a;
}

void crash_two(int b) {
    fake_function *f = (fake_function*)&buf;
    f(b);
}

int main(int argc, char** argv) {
    if(argc < 2) {
        error("program <filename>");
        return -1;
    }

    std::ifstream input(argv[1]);
    if(input.fail()) {
        error("failed to open file!");
        return -1;
    }

    const unsigned BUFSIZE = 1024;
    char argbuf[BUFSIZE];

    input.read(argbuf, BUFSIZE);

    if(
        (memcmp(argbuf, "cat", 3) == 0) ||
        (memcmp(argbuf, "dog", 3) == 0) ||
        (memcmp(argbuf, "bat", 3) == 0) ) {
        crash_one(*(int*)argbuf);
    } else if (
        (memcmp(argbuf, "carrot", 6) == 0) ||
        (memcmp(argbuf, "onion", 5) == 0) ||
        (memcmp(argbuf, "leek", 4) == 0)) {
        crash_two(*(int*)argbuf);
    }

    return 0;
}