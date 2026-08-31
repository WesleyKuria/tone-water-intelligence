/* eslint-disable @typescript-eslint/no-explicit-any */
declare namespace maplibregl {
  export class Map {
    constructor(options?: any);
    on(event: string, callback: (...args: any[]) => void): this;
    on(event: string, layer: string, callback: (...args: any[]) => void): this;
    off(event: string, callback: (...args: any[]) => void): this;
    off(event: string, layer: string, callback: (...args: any[]) => void): this;
    remove(): void;
    fitBounds(bounds: any, options?: any): this;
    flyTo(options: any): this;
    getSource(id: string): any;
    addSource(id: string, source: any): this;
    removeSource(id: string): this;
    addLayer(layer: any, beforeId?: string): this;
    removeLayer(id: string): this;
    getCanvas(): HTMLCanvasElement;
    setFeatureState(feature: any, state: any): void;
    queryRenderedFeatures(pointOrBox?: any, options?: any): any[];
    [key: string]: any;
  }
  export interface GeoJSONSource {
    setData(data: any): void;
    [key: string]: any;
  }
  export class NavigationControl {
    constructor(options?: any);
    [key: string]: any;
  }
  export class Marker {
    constructor(options?: any);
    setLngLat(lngLat: [number, number] | any): this;
    addTo(map: Map): this;
    remove(): this;
    [key: string]: any;
  }
  export class Popup {
    constructor(options?: any);
    setLngLat(lngLat: [number, number] | any): this;
    setHTML(html: string): this;
    addTo(map: Map): this;
    remove(): this;
    [key: string]: any;
  }
  export class LngLatBounds {
    constructor(sw?: any, ne?: any);
    extend(obj: any): this;
    [key: string]: any;
  }
}

declare module 'maplibre-gl' {
  export = maplibregl;
}
