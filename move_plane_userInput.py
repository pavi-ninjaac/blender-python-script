# Example usage for this test.
# /home/pavithra/Pictures/software/blender-3.0.0-linux-x64/blender --factory-startup blend_files/plane.blend -P move_plane_userInput.py -- --value=[[],[],[],[1.0,1.0,1.0]]
       
#
# Notice:
# '--factory-startup' is used to avoid the user default settings from
#                     interfering with automated scene generation.
#
# '--' causes blender to ignore all following arguments so python can use them.
#
# See blender --help for details.


import bpy
import ast
import os

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
    w, h = 100,100
    # image = bpy.types.images
    # scene=bpy.context.scene
    # scene.render.image_settings.file_format='JPEG'
    # image.save_render(os.path.join(output_dir, "img.jpg") ,scene)

    bpy.context.scene.render.image_settings.file_format='JPEG'
    bpy.context.scene.render.resolution_x = w #perhaps set resolution in code
    bpy.context.scene.render.resolution_y = h
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.filepath = os.path.join(output_dir, "img.jpg")
    bpy.ops.render.render(write_still=True)
    print("image saved")

    return 0


def main():
    import sys       # to get command line args
    import argparse  # to parse options for us and print a nice help message

    # get the args passed to blender after "--", all of which are ignored by
    # blender so scripts may receive their own arguments
    argv = sys.argv

    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    # When --help or no args are given, print this help
    usage_text = (
        "Run blender in background mode with this script:"
        "  blender --background --python " + __file__ + " -- [options]"
    )

    parser = argparse.ArgumentParser(description=usage_text)

    # Example utility, add some text and renders or saves it (with options)
    # Possible types are: string, int, long, choice, float and complex.
    parser.add_argument(
        "-v", "--value", dest="values", type=str, required=True,
        help="This text will be used to render an image",
    )


    args = parser.parse_args(argv)  # In this example we won't use the args

    if not argv:
        parser.print_help()
        return

    if not args.values:
        print("Error: --text=\"some string\" argument not given, aborting.")
        parser.print_help()
        return
    else:
        ver_value_list = args.values

    # Run the example function
    ver_value_list = ast.literal_eval(ver_value_list)
    move(ver_value_list)

    print("batch job finished, exiting")


if __name__ == "__main__":
    main()
