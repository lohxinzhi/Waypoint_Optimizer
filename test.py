from waypoint import Region, Plate
from waypoint import CreatePlateScene, printID, visualiseScene
from waypoint import getIntersectRegions, ExcludeTableRegion, LinkRegionAndPlate
from waypoint import getNearestPlate, getBestRegion, updateRegions
import time
from shapely.geometry import Polygon

## Set up plates

plate_coords = [    
        # (0.69136,-0.03378),
        # (0.46042,-0.31386),
        # (0.23854,0.22787),
        # (-0.07518,-0.28684),
        # (-0.20048,0.13328),
        # (0.63731,0.25367),
        # (0.21473,0.04484),
        # (-0.69118,-0.27422),
        # (-0.824,0.26879),
        # (-0.39502,-0.31306),
        # (-0.5668,0.13019),

        [(15.73467022725663,4.466218948364258),
        (15.503726049400663,4.186137711389996),
        (15.281844772651505,4.272131496417579),
        (14.96813210501128,4.213163093905056),
        (14.84283260425964,4.633284949366448),
        (15.680619462226511,4.753670744206264),
        (15.258040753809203,4.544838242953524),
        (14.35212701136407,4.225779916635728),
        (14.219303459865737,4.768794600959865),
        (14.648283560595326,4.186935659441186),
        (14.476506543734645,4.6301875562356365)],

        [(13.788846761961562,4.533781051635742),
        (13.557902584105594,4.813862288610004),
        (13.212228831777495,4.18709084710579),
        (13.085290776414343,4.771634321374693),
        (12.45830597989498,4.460102356771995),
        (13.650095882061686,4.237642064525236),
        (13.344794255771763,4.51380029811026),
        (12.406303546069001,4.774220083364272),
        (12.894614170282706,4.49833653055281),
        (12.726349871289006,4.782659171118309),
        (12.5828062260519,4.191725022755978)],

        [(10.239146684303787,4.484401441717194),
        (10.470090862159754,4.204320204742932),
        (10.691972138908913,4.290313989770515),
        (11.005684806549137,4.231345587257992),
        (11.130984307300778,4.818182497823284),
        (10.293197449333906,4.7718532375592),
        (10.828709644244158,4.797574900561507),
        (11.621689900196348,4.243962409988664),
        (11.754513451694681,4.7869770943128005),
        (11.325533350965092,4.205118152794122),
        (11.497310367825772,4.648370049588572)]
        ]

plates = CreatePlateScene(plate_coords[0]+plate_coords[1]+plate_coords[2])
table = Polygon(((10,4.0),(10, 5.0),(16, 5.0),(16,4.0)))

# for plate in plates:
#     print (f"x = {plate.x}")
#     print (f"y = {plate.y}")
#     print (f"center = {plate.center}")
#     print()  

start_point = (0.0,-1.5) # robot start point

poly_list = [plate.polygon for plate in plates]
centers_list = [plate.center for plate in plates]

print("processing...\n")
start_time = time.time()
x = getIntersectRegions(poly_list)
z = ExcludeTableRegion(x,table)
Z = LinkRegionAndPlate(z, plates)
print("Process time = ",time.time()-start_time)

plates_remain = [plate for plate in plates]

waypoints = [start_point]
count = 0
while len(plates_remain) > 0:
    n1, d1 = getNearestPlate(waypoints[count], plates_remain)
    best_region, best_region_qty, best_region_area = getBestRegion(n1)
    waypoints.append(best_region.center)
    updateRegions(Z, best_region.member_plate)
    plates_remain = [plate for plate in plates_remain if plate.id not in [plate.id for plate in best_region.member_plate]]
    printID(plates_remain)
    print()
    
    count +=1

print(waypoints)

visualiseScene(polygons=z, points=waypoints, show_table=True, table=table, xlim=[8,17], ylim=[2,7])
