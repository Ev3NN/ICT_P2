#include <cmath>
#include <cstddef>
#include <fstream>
#include <functional>
#include <iostream>
#include <unordered_map>
#include <vector>

using bit = int;

// from https://stackoverflow.com/questions/3272424/compute-fast-log-base-2-ceiling
int ceil_log2(unsigned long long x) {
    static const unsigned long long t[6] = {
        0xFFFFFFFF00000000ull,
        0x00000000FFFF0000ull,
        0x000000000000FF00ull,
        0x00000000000000F0ull,
        0x000000000000000Cull,
        0x0000000000000002ull};

    int y = (((x & (x - 1)) == 0) ? 0 : 1);
    int j = 32;
    int i;

    for (i = 0; i < 6; i++) {
        int k = (((x & t[i]) == 0) ? 0 : j);
        y += k;
        x >>= k;
        j >>= 1;
    }

    return y;
}

// std::vector<bit> with a faster hash & comparison
class Word {
    friend class std::hash<Word>;

public:
    Word() = default;

    bit back() const { return body.back(); }
    void pop_back() {
        if (body.back())
            rev_value -= len;
        body.pop_back();
        --len;
    }

    void push_back(bit b) {
        ++len;
        if (b)
            rev_value += len;
        body.push_back(b);
    }

    void clear() {
        body.clear();
        rev_value = 0;
        len = 0;
    }

    bool empty() const { return body.empty(); }

    bool operator==(const Word &o) const {
        if (rev_value != o.rev_value) return false;
        if (len != o.len) return false;
        return body == o.body; // worst case
    }

    const std::vector<bit> &raw() const { return body; }

private:
    std::vector<bit> body;
    std::size_t len, rev_value;
};

// https://stackoverflow.com/questions/17016175/c-unordered-map-using-a-custom-class-type-as-the-key
namespace std {
template <>
struct hash<Word> {
    std::size_t operator()(const Word &k) const {
        return ((std::hash<int>()(k.rev_value) ^ (std::hash<int>()(k.len) << 1)) >> 1);
    }
};
}

template <class WordType>
class LempelZivDict {
public:
    LempelZivDict(const WordType &empty) : dict{}, list{}, next(0) {
        add(empty);
    }

    std::optional<std::size_t> find(const WordType &w) const {
        auto it = dict.find(w);
        if (it == dict.end()) return std::nullopt;
        return it->second;
    }

    bool contains(const WordType &w) const { return dict.find(w) != dict.end(); }

    const WordType &get_word(std::size_t value) const { return list[value]; }

    std::size_t get_value(const WordType &w) const { return dict.find(w)->second; }

    std::size_t add(const WordType &w) {
        dict[w] = next;
        list.push_back(w);
        return next++;
    }

    std::size_t get_next_address() const { return next; }

private:
    std::unordered_map<WordType, std::size_t> dict;
    std::vector<WordType> list;
    std::size_t next;
};

class Encoder {
public:
    Encoder() : encoded{}, current{}, dict(current), last_address(0) {}

    void encode(const std::vector<bit> &message);

    const std::vector<bit> &get_encoded() const { return encoded; }
    const LempelZivDict<Word> &get_dict() const { return dict; }

private:
    std::vector<bit> encoded;
    Word current;
    LempelZivDict<Word> dict;

    std::size_t last_address;

    void read(bit b);
    void finish();
};

void Encoder::encode(const std::vector<bit> &message) {
    for (bit b : message)
        read(b);
    finish();
}

void Encoder::read(bit b) {
    current.push_back(b);
    auto curr_addr = dict.find(current);

    if (!curr_addr.has_value()) {
        std::size_t addr = dict.add(current);
        if (addr == 1) {
            encoded.push_back(b);
        } else {
            int addr_len = ceil_log2(addr);
            for (addr_len--; addr_len >= 0; addr_len--)
                encoded.push_back((last_address >> addr_len) & 1);
            encoded.push_back(b);
        }
        current.clear();
        last_address = 0;
    } else {
        last_address = *curr_addr;
    }
}

void Encoder::finish() {
    if (current.empty())
        return;

    // add rest
    bit b = current.back();
    current.pop_back();

    std::size_t pre_addr = dict.get_value(current);
    int addr_len = ceil_log2(dict.get_next_address());
    for (addr_len--; addr_len >= 0; addr_len--)
        encoded.push_back((pre_addr >> addr_len) & 1);
    encoded.push_back(b);
}

std::vector<bit> decode(const std::vector<bit> &msg) {
    // at pos 0 there is the empty word
    std::vector<std::vector<bit>> reverse_dict{{}};
    std::vector<bit> decoded{};

    auto it = msg.begin();
    auto end = msg.end();

    // once 0 bit address
    decoded.push_back(*it);
    reverse_dict.push_back(decoded);
    ++it;

    std::size_t len = 1;
    int count_bkp = 1;

    // 1* 1 bit address
    // 2* 2 bit
    // 4* 3 bit
    // ...

    for (int count = count_bkp; it != end; ++it, --count) {
        if (count == 0) {
            count_bkp *= 2;
            count = count_bkp;
            len += 1;
        }

        // build addr from the bits
        std::size_t addr = 0;
        for (int shift = len - 1; shift >= 0; --shift, ++it)
            addr += (*it << shift);

        // get prefix, add last bit
        std::vector<bit> word = reverse_dict[addr];
        word.push_back(*it);

        // add word to decoded
        decoded.insert(decoded.end(), word.begin(), word.end());

        // add word to dict
        reverse_dict.push_back(std::move(word));
    }

    return std::move(decoded);
}

template <class T>
std::ostream &operator<<(std::ostream &out, const std::vector<T> &v) {
    out << '[';
    if (v.empty())
        return out << ']';
    auto it = v.begin();
    auto end = v.end();
    out << *it;
    for (++it; it != end; ++it)
        out << ", " << *it;
    return out << ']';
}

void course_example() {
    using namespace std;
    // [[1], [0, 0], [0, 1, 1], [1, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    vector<bit> msg{1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0};
    Encoder example;
    example.encode(msg);
    // cout << example.get_encoded() << endl;

    cout << "original length: " << msg.size() << endl;
    cout << "compressed length: " << example.get_encoded().size() << endl;

    vector<bit> msg_decoded = decode(example.get_encoded());
    // cout << msg_decoded << endl;
    if (msg_decoded != msg)
        cerr << "msg error!" << endl;
}

void genome_ascii() {
    using namespace std;

    ifstream f("genome.txt");
    if (!f.is_open()) {
        cerr << "unable to open file!" << endl;
        exit(1);
    }

    // skip newline, keep byte encoding for other
    char c;
    int count = 0;
    vector<bit> genome;
    while (f >> c) {
        if (--count == 0) break;
        if (c == '\n')
            continue;
        for (int k = 7; k >= 0; k--)
            genome.push_back((c >> k) & 1);
    }

    Encoder genome_enc;
    genome_enc.encode(genome);
    const vector<bit> &encoded = genome_enc.get_encoded();

    // 7668456
    cout << "original length: " << genome.size() << endl;
    // 3243053
    cout << "compressed length: " << encoded.size() << endl;
    // ratio: 7668456/3243053 ~ 2.36

    // they match :)
    //const vector<bit> decoded = decode(encoded);
    //if (decoded != genome)
    //    cerr << "decoded do not match raw!";
}

void genome_bin() {
    using namespace std;

    ifstream f("genome.txt");
    if (!f.is_open()) {
        cerr << "unable to open file!" << endl;
        exit(1);
    }

    // better re-encoding to have shorter input
    char c;
    int count = 0;
    vector<bit> genome;
    while (f >> c) {
        if (--count == 0) break;
        switch (c) {
        case 'A':
            genome.push_back(0);
            genome.push_back(0);
            break;
        case 'T':
            genome.push_back(0);
            genome.push_back(1);
            break;
        case 'C':
            genome.push_back(1);
            genome.push_back(0);
            break;
        case 'G':
            genome.push_back(1);
            genome.push_back(1);
            break;
        case '\n':
            continue;
        default:
            break;
        }
    }

    Encoder genome_enc;
    genome_enc.encode(genome);
    const vector<bit> &encoded = genome_enc.get_encoded();

    // 1917114
    cout << "original length: " << genome.size() << endl;
    // 2095205
    cout << "compressed length: " << encoded.size() << endl;
    // ratio: 1917114/2095205 ~ 0,91500068

    // they match :)
    //const vector<bit> decoded = decode(encoded);
    //if (decoded != genome)
    //    cerr << "decoded do not match raw!";
}

int main() {
    using namespace std;
    cout << "example" << endl;
    course_example();

    cout << "genome (ascii)" << endl;
    genome_ascii();

    cout << "genome (bin)" << endl;
    genome_bin();
}