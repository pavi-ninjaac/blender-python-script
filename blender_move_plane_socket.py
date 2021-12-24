import bpy
import ast
import os
import socket

def move(ver_value_list):
    # ver_value_list = [[],[], [] , [1.0, 1.0, 1.0]]
    # selected object
    so = bpy.context.active_object

    # so.data.vertices[0] = Vector((1,1,1))
    # print([v.co for v in so.data.vertices])

    # print("the value passed",ver_value_list, type(ver_value_list))
    for v in so.data.vertices:
        # vertex value will be like [[1.0,2.0,0.0], [1.0,0.0,0.0], [] , [0.0,0.0,0.0]] ## it is a plane so 4 vertices this time
        # print(v.index,v)
        if ver_value_list[v.index] == []: 
            # when i don't want to change certine index leave it empty 
            # ---> t will be in it's current point no chnages
            continue
        else:
            vertex_value_to_change = ver_value_list[v.index]
            v.co.x += vertex_value_to_change[0]
            v.co.y += vertex_value_to_change[1]
            v.co.z += vertex_value_to_change[2]
    # print([v.co for v in so.data.vertices])

    # save the current scene as image
    output_dir = "/home/pavithra/Pictures/learning/blender/opencv_live_movement_checking/"
    
    # set te image resolution
    w, h = 500,500

    # change the sample render size in render properties.
    bpy.context.scene.eevee.taa_render_samples = 32
    bpy.context.scene.render.film_transparent = True
    # change the render engine to cycle.
    bpy.context.scene.render.engine = "BLENDER_EEVEE"

    # Disable soft shadow at shadows at render properties.
    bpy.context.scene.eevee.use_soft_shadows = False
    bpy.context.scene.eevee.sss_samples = 4
    bpy.context.scene.eevee.volumetric_samples = 32
    bpy.context.scene.render.simplify_gpencil_antialiasing = False
    # Disable the shadow in the visibility Display at Object properties.
    bpy.context.object.display.show_shadows = False

    # setting for transperacy.
    #bpy.context.scene.render.image_settings.file_format='PNG'
    #bpy.context.scene.render.image_settings.color_mode ='RGBA'
    bpy.context.scene.render.film_transparent = True

    bpy.context.scene.render.resolution_x = w #perhaps set resolution in code
    bpy.context.scene.render.resolution_y = h
    bpy.context.scene.render.resolution_percentage = 100

    # Set the camera view settings.
    bpy.data.objects['Camera'].data.shift_x = 0.24 # move camera to left-right position.
    bpy.data.objects['Camera'].data.shift_y = 0.22 # move camera up-bottom position.
    bpy.data.objects['Camera'].data.sensor_width = 40 # camera focus.
    
    # save the image.
    bpy.context.scene.render.filepath = os.path.join(output_dir, "img.jpg")
    bpy.ops.render.render(write_still=True)
    print("image saved")

    return 0

def start_server(): 
    host = ""
    port = 49411

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
        except socket.error as msg:
            print("Error while binding the server:", msg[1])
        while True:
            print("The server listernig on all host and port",port)
            s.listen()
            conn, add = s.accept()
            with conn:
                print("connected by", add)
                data_from_client = conn.recv(1024).decode() # recieved data also byte --> so meed decoding here
                if data_from_client == 'end':
                    print("Ending the blender server connection")
                    conn.send("Connection Ended".encode())
                    break
                else: # when it has some list of vertice value ---> need processing
                    print("processing data ...")
                    ver_value_list = ast.literal_eval(data_from_client)
                    print(ver_value_list,"value from the client and its type", type(ver_value_list))
                    move(ver_value_list)
                    conn.send("success".encode()) # sending value should be byte--> so needed to be encoded


if __name__ == "__main__":
    start_server()




w,h = 500, 500
output_dir = "/home/pavithra/Pictures/learning/blender/opencv_live_movement_checking/"
bpy.context.scene.render.resolution_x = w #perhaps set resolution in code
bpy.context.scene.render.resolution_y = h
bpy.context.scene.render.resolution_percentage = 100

bpy.context.object["Cameras"].data.shift_x = 0.24
bpy.context.object.data.shift_y = 0.22
bpy.context.object.data.sensor_width = 40
    
 # save the image.
bpy.context.scene.render.filepath = os.path.join(output_dir, "img.jpg")
bpy.ops.render.render(write_still=True)
print("image saved")