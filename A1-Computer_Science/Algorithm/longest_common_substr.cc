#include <bits/stdc++.h>
/*
Longest common substring:
    If the selected character equals, then the count of this dp[i][j] = dp[i-1][j-1] + 1
    else, the count of this dp equals zero.

The dp means that the length of longest common substring which ends with current coordinate.
*/
using namespace std;

vector<string> longest_common_substr(string a, string b) {
    vector<vector<int>> dp(a.size() + 1, vector<int>(b.size() + 1, 0));
    int max_size = 0;
    vector<string> result;
    for (int i = 1; i <= a.size(); i++) {
        for (int j = 1; j <= b.size(); j++) {
            if (a[i - 1] == b[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > max_size) {
                    max_size = dp[i][j];
                }
            }
        }
    }
    if (max_size == 0) {
        return result;
    }
    for (int i = 1; i <= a.size(); i++) {
        for (int j = 1; j <= b.size(); j++) {
            if (dp[i][j] == max_size) {
                result.push_back(string(a.begin() + i - max_size, a.begin() + i));
            }
        }
    }

    return result;
}

int main() {
    string a = "ueoa", b = "aoeu";
    for (auto i : longest_common_substr(a, b)) {
        cout << i << endl;
    }
    return 0;
}
