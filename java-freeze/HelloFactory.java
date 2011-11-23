public class HelloFactory
    implements Ice.ObjectFactory {

    public Ice.Object create(String type) {
        return new HelloI();
    }

    public void destroy() {}
}
