import json
import os
import urllib
from addict import Dict
from folium import folium, features
import folium
import requests
from PIL import Image, ImageDraw
from io import BytesIO

class ShapeOperations:
    """
    Shape Operatings
    Draw Line
    Add Point
    """
    def __init__(self, map, file_id):
        self.map = map
        self.file_id = file_id

    def draw_bounding_boxes(self, url_list, bbox_set):
        """
        Draws bounding boxes on images and saves them to a directory.

        Args:
            url_list (list): A list of CDN or local path URLs for images.
            bbox_set (set): A set of bounding box coordinates for objects in the images.

        Returns:
            drawing (list): A list of file paths to the saved images with bounding boxes.
        """
        drawing = []
        for i, key in enumerate(bbox_set):
            if url_list[i][2].startswith("http"):
                image = Image.open(os.path.join("Exports",self.file_id,os.path.basename(url_list[i][2])))
            else:
                image = Image.open(url_list[i][2])
            draw = ImageDraw.Draw(image)
            draw.rectangle(url_list[i][1], width=2, outline="red")
            image_path = os.path.join('Exports', self.file_id, f"Obj-{key}.jpg")
            image.save(image_path)
            drawing.append([os.path.join(f"Obj-{key}.jpg"),url_list[i][3]])

        return drawing

    def addPoint(self, kwargs: Dict,
                 area: float = None,
                 color: str = 'darkgreen',
                 type: str = 'point'):
        """
        Add point
        """
        if type == 'point':
            image_paths = set()
            obj_ids = set()
            img_urls = set()
            params = Dict(kwargs)
            links = []
            bbox_obj = []
            new_list = []
            int_keys = [key for key in params.point if isinstance(key, int)]
            for i, matched_point in zip(range(2, max(int_keys) + 1, 2), params.geojson.matchedPoints):
                if i in params.point:
                    area = "{:.3f}".format(float(area))
                    html = "<section class='container' style='width:450px'> \
                                <div class='value'> \
                                    <b>Area = </b> {area} square meter </br>\
                                    <b>Classname = </b> {classname} </br>\
                                    <b>Toplam intersect = </b> {Toplamintersect} </br>\
                                </div>" \
                        .format(area=area,
                                classname=params.point.classname,
                                Toplamintersect=i / 2)
                    objectImage_1 = os.path.join(os.getcwd(), params.point[i].detectedPath_1)
                    objectImage_2 = os.path.join(os.getcwd(), params.point[i].detectedPath_2)
                    objId_1 = params.point[i].objId_1
                    objId_2 = params.point[i].objId_2
                    imgUrl_1 = params.point[i].imgUrl_1
                    imgUrl_2 = params.point[i].imgUrl_2
                    image_paths.add(objectImage_1)
                    image_paths.add(objectImage_2)
                    obj_ids.add(objId_1)
                    obj_ids.add(objId_2)
                    img_urls.add(imgUrl_1)
                    img_urls.add(imgUrl_2)

                    html += "<div class='image-container'>"
                    for path in image_paths:
                        html += f"<img src='{path}' style='width:auto;height:80px;'>"
                    html += "</div>"
                    links.append([params.point[i].objId_1, params.point[i].imgUrl_1])
                    links.append([params.point[i].objId_2, params.point[i].imgUrl_2])
                    bbox_obj.append([matched_point.properties['objId_1'], matched_point.properties['bbox_1'],matched_point.properties['score_1']])
                    bbox_obj.append([matched_point.properties['objId_2'], matched_point.properties['bbox_2'],matched_point.properties['score_2']])

            result = []
            for obj_id1 in links:
                for obj_id2 in bbox_obj:
                    if obj_id1[0] == obj_id2[0]:
                        result.append([obj_id2[0], obj_id2[1], obj_id1[1],obj_id2[2]])

            for key, element in enumerate(result):
                if element not in new_list:
                    new_list.append(element)
            objects = self.draw_bounding_boxes(new_list, obj_ids)
            html += "<div class='url-container'>"
            for url, obj in zip(objects, obj_ids):
                html += f"<a href='{url[0]}'>Object Location</a>"f"<b> | ObjectId={obj}</b> | <b>Score={round(url[1],2)}</b></br>"

            html += "<div class='value'>"
            html += "</div>"
            svg_icon_path = os.path.join(os.getcwd(), 'Config', 'icon', params.point.classname + '.png')

            icon = folium.DivIcon(html=f"""
                                            <div>
                                            <img src = "{svg_icon_path}" width="30px" "/>
                                            </div>""")

            mk = features.Marker([params.point.Lat_center, params.point.Lon_center],
                                 popup=html, icon=icon)

            mk_p = folium.Circle([params.point.Lat_center, params.point.Lon_center],  # noqa
                                 radius=2,
                                 fill=True,
                                 fill_color="yellow",
                                 color="yellow",
                                 fill_opacity=0.4)

            self.map.add_child(mk)
            self.map.add_child(mk_p)

        if type == 'paired':
            for point in kwargs:
                mk = features.Marker(point,
                                     popup=None, icon=folium.Icon(color=color, icon_color='#FFFF00'))

                self.map.add_child(mk)

    def addPolyline(self, des, classname, obj, color):
        """
        Poly line drawing
        """
        folium.PolyLine(
            locations=des,
            color=color,
            opacity=4,
            tooltip=classname + "-" + str(obj),
            weight=4
        ).add_to(self.map)
        pass

    def triggerMapOperations(self, mapDrawPoint):
        """
        processing coming point data
        """

        for key, params in mapDrawPoint.items():
            params = Dict(params)
            if params.mapOp == "polyline":
                self.addPolyline(des=params.desPoint, classname=params.classname, obj=key, color=params.color)
            elif params.mapOp == "point":
                self.addPoint(kwargs=params, area=params.object['area'], color="red", type=params.mapOp)
            elif params.mapOp == "paired":
                pass
                # self.addPoint(kwargs=params.pairedPoint, area=None, color="gray", type=params.mapOp)
            else:
                continue
