import ee

try:
    ee.Initialize()
except Exception:
    ee.Authenticate()  # Opens a browser for you to login and grant permission
    ee.Initialize()


def get_aoi(lat, lon, buffer_km):
    # Convert buffer_km to meters
    buffer_m = buffer_km * 1000
    point = ee.Geometry.Point([lon, lat])
    return point.buffer(buffer_m).bounds()

def download_sentinel1(aoi, start_date, end_date):
    collection = (ee.ImageCollection('COPERNICUS/S1_GRD')
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .select(['VV', 'VH']))

    sentinel1_img = collection.median().clip(aoi)
    return sentinel1_img

def download_sentinel2(aoi, start_date, end_date):
    collection = (ee.ImageCollection('COPERNICUS/S2_SR')
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        .select(['B2', 'B3', 'B4', 'B8']))  # Blue, Green, Red, NIR bands

    sentinel2_img = collection.median().clip(aoi)
    return sentinel2_img

def get_download_url(image, aoi, scale=10):
    url = image.getDownloadURL({
        'scale': scale,
        'region': aoi,
        'fileFormat': 'GeoTIFF'
    })
    return url

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download Sentinel-1 SAR and Sentinel-2 Optical imagery")
    parser.add_argument('--lat', type=float, required=True, help='Latitude of AOI center')
    parser.add_argument('--lon', type=float, required=True, help='Longitude of AOI center')
    parser.add_argument('--buffer', type=float, default=10, help='AOI buffer in km')
    parser.add_argument('--start', type=str, required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, required=True, help='End date (YYYY-MM-DD)')

    args = parser.parse_args()


    aoi = get_aoi(args.lat, args.lon, args.buffer)

    print(f"Downloading Sentinel-1 SAR data for AOI centered at ({args.lat},{args.lon}) from {args.start} to {args.end}")
    s1_img = download_sentinel1(aoi, args.start, args.end)
    s1_url = get_download_url(s1_img, aoi)
    print("Sentinel-1 download URL:", s1_url)

    print(f"Downloading Sentinel-2 Optical data for AOI centered at ({args.lat},{args.lon}) from {args.start} to {args.end}")
    s2_img = download_sentinel2(aoi, args.start, args.end)
    s2_url = get_download_url(s2_img, aoi)
    print("Sentinel-2 download URL:", s2_url)
