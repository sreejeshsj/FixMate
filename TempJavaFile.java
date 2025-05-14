import java.util.*;

public class LetterCombinations {
    public static List<String> letterCombinations(String digits) {
        Map<Character, String> map = new HashMap<>();
        map.put('2', "abc");
        map.put('3', "def");
        map.put('4', "ghi");
        map.put('5', "jkl");
        map.put('6', "mno");
        map.put('8', "tuv");
        map.put('9', "wxyz");
        
        List<String> res = new ArrayList<>();
        if (digits == null || digits.length() == 0) return res;
        
        dfs(digits, 0, new StringBuilder(), res, map);
        return res;
    }
    
    private static void dfs(String digits, int index, StringBuilder curStr, List<String> res, Map<Character, String> map) {
        if (curStr.length() == digits.length()) {
            res.add(curStr.toString());
            return;
        }
        
        String letters = map.get(digits.charAt(index));
        if (letters != null) {
            for (char c : letters.toCharArray()) {
                curStr.append(c);
                dfs(digits, index + 1, curStr, res, map);
                curStr.deleteCharAt(curStr.length() - 1);
            }
        }
    }
    
    public static void main(String[] args) {
        System.out.println(letterCombinations("23"));
    }
}
