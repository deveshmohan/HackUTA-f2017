#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include "libfreenect/libfreenect.h"

#define DEBUG(...) fprintf(stderr, __VA_ARGS__)

int frames = 0;
uint8_t* depth_frame;
uint8_t* video_frame;
const char *tmpname_video = "/tmp/kinect.video";
const char *tmpname_depth = "/tmp/kinect.depth";
bool write_frame = true;

typedef struct {
	FILE *output;
	bool is_depth;
	bool video_started;
	bool depth_started;
} user_data;

void encode_depth(uint16_t *depth_in, uint8_t *rgb_out, size_t n) {
	/* Based on libfreenect/examples/glview.c */
	DEBUG ("Encoding depth frame\n");
	bool nonzero = false;
	for (int i = 0; i++; i < n) {
		if (depth_in[i]) {nonzero = true;}
		uint8_t grey = (depth_in[i] >> 3) & 0xFF;
		rgb_out[3*i+0] = grey;
		rgb_out[3*i+1] = grey;
		rgb_out[3*i+2] = grey;
	}
	if (nonzero) {
		DEBUG ("Nonzero value in frame!\n");
	}
}


void rgb_callback(freenect_device *dev, void *rgb, uint32_t time) {
	DEBUG ("Received video frame\n");
	fwrite(rgb, sizeof(uint8_t), 640*480*3, ((user_data*) freenect_get_user(dev))->output);
	if (write_frame) {
		FILE *video_file = fopen(tmpname_video, "wb");
		fwrite(rgb, sizeof(uint8_t), 640*480*3, video_file);
		fclose(video_file);
	}
	frames++;
}

void depth_callback(freenect_device *dev, void *data, uint32_t time) {
	DEBUG ("Received depth frame\n");
	encode_depth((uint16_t*) data, depth_frame, 480*640);
	fwrite(depth_frame, sizeof(uint8_t), 480*640*3, ((user_data*) freenect_get_user(dev))->output);
	frames++;
}

void start_capture(freenect_device *device) {
	user_data* udata = (user_data*) freenect_get_user(device);
	DEBUG ("Capture started on %s\n", udata->is_depth ? "depth" : "video");
	if (udata->is_depth){
		udata->video_started && freenect_stop_video(device);
		udata->depth_started || freenect_start_depth(device);
		udata->depth_started = true;
		udata->video_started = false;
	} else {
		udata->depth_started && freenect_stop_depth(device);
		udata->video_started || freenect_start_video(device);
		udata->video_started = true;
		udata->depth_started = false;
	}
}

void stop_capture(freenect_device *device) {
	DEBUG ("Capture stopped\n");
	user_data* udata = (user_data*) freenect_get_user(device);
	udata->depth_started && freenect_stop_depth(device);
	udata->video_started && freenect_stop_video(device);
	udata->depth_started = false;
	udata->video_started = false;
}
		
int main(int argc, char **argv) {
	freenect_context *context;
	if (freenect_init(&context, NULL) < 0) {
		fprintf(stderr, "Unable to create freenect context\n");
		return 1;
	}
	int device_count = freenect_num_devices(context);
	if (device_count <= 0) {
		fprintf(stderr, "No kinect device found\n");
		return 2;
	}
	freenect_select_subdevices(context, (freenect_device_flags)FREENECT_DEVICE_CAMERA);
	freenect_device *device;
	if (freenect_open_device(context, &device, 0) < 0) {
		fprintf(stderr, "Error opening device\n");
		freenect_shutdown(context);
		return 1;
	}
	freenect_set_video_callback(device, rgb_callback);
	freenect_set_depth_callback(device, depth_callback);
        freenect_set_video_mode(device, freenect_find_video_mode(FREENECT_RESOLUTION_MEDIUM, FREENECT_VIDEO_RGB));
        freenect_set_depth_mode(device, freenect_find_depth_mode(FREENECT_RESOLUTION_MEDIUM, FREENECT_DEPTH_11BIT));
	freenect_set_led(device, LED_RED);
	user_data udata;
	udata.output = stdout;
	udata.video_started = false;
	udata.depth_started = false;
	udata.is_depth = (argc > 1 && strcmp(argv[1], "depth") == 0);
	freenect_set_user(device, (void*) &udata);
	depth_frame = malloc(480*640*3*sizeof(uint8_t));
	video_frame = malloc(480*640*3*sizeof(uint8_t));
	freenect_set_video_buffer(device, video_frame);
	start_capture(device);
	while (freenect_process_events(context) >= 0) {}
	stop_capture(device);
	freenect_close_device(device);
	freenect_shutdown(context);
	return 0;
}
