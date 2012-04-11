public class CounterFactory implements Ice.ObjectFactory {
    public Ice.Object create(String type) {
        return new CounterI();
    }

    public void destroy() {}
}
