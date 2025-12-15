import L from "leaflet";

/**
 * Leaflet configuration and utilities
 * Handles common setup issues and provides reusable map functionality
 */

// Fix for default markers in react-leaflet
// This resolves the issue where default marker icons don't load properly
export function initializeLeafletIcons() {
  delete (L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })
    ._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl:
      "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
    iconUrl:
      "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
    shadowUrl:
      "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
  });
}

export const MAP_CONFIG = {
  DEFAULT_CENTER: { lat: 50.06143, lng: 19.93658 },
  DEFAULT_ZOOM: 13,
  DEFAULT_WIDE_ZOOM: 6,
  DEFAULT_HEIGHT: "300px",
  TILE_LAYER_URL: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
  TILE_LAYER_ATTRIBUTION:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
} as const;

export function createPeakIcon(size = 24, color = "blue") {
  const svg =
    `<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">` +
    `<path d="M2 20 L12 3 L22 20 Z" fill="${color}" />` +
    `</svg>`;

  const html = `<span style="display:inline-block;line-height:0">${svg}</span>`;

  return L.divIcon({
    className: "peek-peak-icon",
    html,
    iconSize: [size, size],
    iconAnchor: [Math.floor(size / 2), Math.floor(size * 0.7)],
  });
}
