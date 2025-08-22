Includes = {
}

PixelShader =
{
	Samplers =
	{
		MainTexture =
		{
			Index = 0
			MagFilter = "Linear"
			MinFilter = "Linear"
			MipFilter = "None"
			AddressU = "Clamp"
			AddressV = "Clamp"
		}
	}
}

VertexStruct VS_INPUT
{
	float3 vPosition  : POSITION;
	float2 vTexCoord  : TEXCOORD0;
};

VertexStruct VS_OUTPUT
{
	float4  vPosition : PDX_POSITION;
	float2  vTexCoord : TEXCOORD0;
};

ConstantBuffer( 0, 0 )
{
	float4x4 WorldViewProjectionMatrix;
	float4 Color;
	float2 ShadowOffset; // X and Y offset for shadow in UV space
	float4 ShadowColor;  // RGBA for shadow
};

VertexShader =
{
	MainCode VertexShader
	[[
		VS_OUTPUT main(const VS_INPUT v )
		{
			VS_OUTPUT Out;
			Out.vPosition  = mul( WorldViewProjectionMatrix, float4( v.vPosition.xyz, 1 ) );
			Out.vTexCoord  = v.vTexCoord;
			return Out;
		}
	]]
}

PixelShader =
{
	MainCode PixelShaderDropShadow
	[[
		float4 main( VS_OUTPUT v ) : PDX_COLOR
		{
			// Set default values if not provided by engine
			float2 shadowOffset = ShadowOffset;
			float4 shadowColor = ShadowColor;
			// If both are zero, set defaults
			if (all(shadowOffset == float2(0.0, 0.0))) {
				shadowOffset = float2(0.01, 0.01); // default offset
			}
			if (all(shadowColor == float4(0.0, 0.0, 0.0, 0.0))) {
				shadowColor = float4(0.0, 0.0, 0.0, 0.5); // default: semi-transparent black
			}
			// Sample shadow (offset, usually black and semi-transparent)
			float4 Shadow = tex2D( MainTexture, v.vTexCoord + shadowOffset );
			Shadow *= shadowColor;
			// Sample main texture
			float4 OutColor = tex2D( MainTexture, v.vTexCoord );
			OutColor *= Color;
			// Alpha blend shadow and main
			float alpha = OutColor.a + Shadow.a * (1 - OutColor.a);
			float3 rgb = (OutColor.rgb * OutColor.a + Shadow.rgb * Shadow.a * (1 - OutColor.a)) / max(alpha, 0.0001);
			return float4(rgb, alpha);
		}
	]]
}

BlendState BlendState
{
	BlendEnable = yes
	AlphaTest = no
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
}

Effect DropShadow
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderDropShadow"
}
