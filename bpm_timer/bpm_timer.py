import bpy

obj = bpy.data.objects["Light"].data
modifier = bpy.context.object.modifiers["NetworkModifier"]


frame = 10



def setJump(size, frame):
    modifier["Socket_8"] = 1 
    modifier.keyframe_insert(data_path='["Socket_8"]', frame=frame - 2) 
    obj.energy = 300
    obj.keyframe_insert(data_path="energy", frame=frame - 2)

    modifier["Socket_8"] = 11
    modifier.keyframe_insert(data_path='["Socket_8"]', frame=frame)
    obj.energy = size
    obj.keyframe_insert(data_path="energy", frame=frame)
    
    modifier["Socket_8"] = 1 
    modifier.keyframe_insert(data_path='["Socket_8"]', frame=frame + 2) 
    obj.energy = 300
    obj.keyframe_insert(data_path="energy", frame=frame + 2)


def getPeaks(bpm, fps, start_frame, end_frame):
    beat_per_second = bpm / 60.0
    keyframes_per_second = fps / beat_per_second
    
    frames = end_frame - start_frame  
    frame_times = frames / keyframes_per_second
    
    round_keyframes = []
    for keyframes in range(int(frame_times) + 2): 
        time = start_frame + (keyframes * keyframes_per_second)
        round_keyframes.append(round(time))    
        
    for keyframe in round_keyframes:
        value = 600
        setJump(value, keyframe)
    
        
bpm = 174
fps = bpy.context.scene.render.fps
start_frame, end_frame = bpy.context.scene.frame_start, bpy.context.scene.frame_end
getPeaks(bpm, fps, start_frame, end_frame)
