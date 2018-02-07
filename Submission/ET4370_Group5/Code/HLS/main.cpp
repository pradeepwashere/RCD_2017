#include <stdint.h>
#include <hls_stream.h>
#include <ap_axi_sdata.h>

#define WIDTH 1280
#define HEIGHT 720


typedef ap_axiu<32,1,1,1> pixel_data;
typedef hls::stream<pixel_data> pixel_stream;

void stream_g(pixel_stream &src, pixel_stream &dst)
{
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE axis port=&src
#pragma HLS INTERFACE axis port=&dst


#pragma HLS PIPELINE II=1

    static uint32_t gray,R,G,B;
    static uint32_t x = 0; // pixel count
    static uint32_t y = 0; // Line Number
    static uint32_t threshold_min = 15;
    static uint32_t threshold_max = 250;
    static uint32_t diff = 235;

    static pixel_data p_out;
    static pixel_data g_in;

//-----------------------------------------

    pixel_data p_in; // input stream
    src >> p_in;

    R = ((p_in.data)&0x000000FF);
    G = (((p_in.data)&0x0000FF00)>>8);
    B = (((p_in.data)&0x00FF0000)>>16);
    gray = (B*0.30 + G*0.59 +  R* 0.11); // 8 BIT NUMBER- type cast it to 32 bit format

    //if(gray>255)
	//gray=255;

    if(gray > threshold_max)
        gray = 255;
    else if(gray < threshold_min)
        gray = 0;
    else
        gray = (threshold_max * (gray - threshold_min))/diff;

    g_in = p_in;
    g_in.data = ((((gray<<24)&0xFF000000)|((gray<<16)&0x00FF0000)|((gray<<8)&0x0000FF00)|((gray)&0x000000FF)));
    p_in = g_in;

//------------------------------------------

	if (p_in.user) // CHeck starting of the frame
		x = y = 0;

//-------------------------------------------

    p_out = p_in;

//----------------------------------------------

    dst << p_out; // output the data

//----------------------------------------------

	if (p_in.last)
	{
		x = 0;
		y++;
	}
	else
		x++;
}
