import bpy

obj = bpy.context.object
 
frame = 10


def setJump(size, frame):
    obj.scale = (1.0, 1.0, 1.0)
    obj.keyframe_insert(data_path="scale", frame=frame - 2)
    obj.scale = size
    obj.keyframe_insert(data_path="scale", frame=frame)
    obj.scale = (1.0, 1.0, 1.0)
    obj.keyframe_insert(data_path="scale", frame=frame + 2)


def getPeaks(bpm, fps, start_frame, end_frame):
    beat_per_second = bpm / 60.0
    keyframes_per_second = fps / beat_per_second
    
    frames = end_frame - start_frame
    frame_times = frames / keyframes_per_second
    
    round_keyframes = []
    for keyframes in range(int(frame_times)): 
        time = start_frame + (keyframes * keyframes_per_second)
        round_keyframes.append(round(time))    
        
    for keyframe in round_keyframes:
        scale = 1.5
        setJump((scale, scale, scale), keyframe)
    
        
bpm = 174
fps = bpy.context.scene.render.fps
start_frame, end_frame = bpy.context.scene.frame_start, bpy.context.scene.frame_end
getPeaks(bpm, fps, start_frame, end_frame)