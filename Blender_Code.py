# George Dimitriadis
# Made on 10/12/2021
# This is the script used in Blender for Blender to read the required numpy arrays and animate tarnsforms and colours
# appropriately. Use Blender 3.0.0

import bpy
import numpy as np

vac_file_name = r"E:\Projects Small\2022_01_Europe_vaccinated_infographic\vaccinated.npy"
vac_array = np.load(vac_file_name)

deaths_file_name = r"E:\Projects Small\2022_01_Europe_vaccinated_infographic\deaths.npy"
deaths_array = np.load(deaths_file_name)

dates_file_name = r"E:\Projects Small\2022_01_Europe_vaccinated_infographic\dates.npy"
dates_array = np.load(dates_file_name, allow_pickle=True)

start_of_vaccination_index = 320


for obj_i, obj in enumerate(bpy.data.collections['Meshes'].objects):

    mat = bpy.data.materials.new(name='colour_of_{}'.format(obj.name))
    mat.shadow_method = 'NONE'
    obj.active_material = mat

    for vac_i in np.arange(vac_array.shape[0]):

        frame = start_of_vaccination_index + vac_i

        vaccinated = vac_array[vac_i, obj_i] / np.max(vac_array)

        mat.diffuse_color = [1 - vaccinated, vaccinated, 0, 1]
        mat.keyframe_insert(data_path = 'diffuse_color', frame=frame, index=-1)

print('Done Mat')

for hook_i, hook in enumerate(bpy.data.collections['Hooks'].objects):

    for death_i in np.arange(deaths_array.shape[0]):
        height = 5 * deaths_array[death_i, hook_i] / np.max(deaths_array)
        hook.location.z = height
        hook.keyframe_insert(data_path = 'location', frame = death_i)

print('Done Height')

def update_date(self):
    date_text_obj = bpy.context.scene.objects['Date']
    frame = bpy.context.scene.frame_current
    date_text_obj.data.body = dates_array[frame]


bpy.app.handlers.frame_change_pre.append(update_date)

for i in np.arange(bpy.context.scene.frame_end):
    bpy.context