// Medallion: Bronze | Mutation: 0% | HIVE: I
/**
 * P3 DELIVER: Golden Layout Adapter
 * Adapts the Golden Layout 2.6 library to the HFO Port 3 interface.
 */

export class GoldenLayoutAdapter {
    private layout: any;
    private container: HTMLElement;

    constructor(container: HTMLElement, goldenLayoutLib: any) {
        this.container = container;
        this.layout = new goldenLayoutLib(this.container);
    }

    /**
     * Register a component with the layout engine
     */
    public registerComponent(name: string, factory: (container: any, state: any) => void) {
        this.layout.registerComponentFactoryFunction(name, factory);
    }

    /**
     * Initialize the layout with a specific configuration
     */
    public init(config: any) {
        this.layout.loadLayout(config);
    }

    /**
     * Update layout size (useful for window resize events)
     */
    public updateSize() {
        this.layout.updateSize();
    }

    /**
     * Get the underlying Golden Layout instance
     */
    public getRawInstance() {
        return this.layout;
    }
}
