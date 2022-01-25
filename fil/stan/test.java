public class test {
    public static void main(String[] args) {
        char[] letters = { 'c', 'f', 'j'};
        char target = 'c';
        int l = 0 , h = letters.length;
        int k = 0;
        int pos = 0;
        while (l<h) {
            k = (l+h)/2;
            if(letters[k] == target) {
                pos = k;
                break;
            }
            else if(letters[k] < target) {
                h=k;
            }
            else{
                l=k;
            }
        }
        System.out.println(letters[pos]);
        System.out.print("kmkm");
    }
}
