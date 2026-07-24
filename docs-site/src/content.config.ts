import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { docsLoader } from "@astrojs/starlight/loaders";
import { docsSchema } from "@astrojs/starlight/schema";

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: z.object({
        category: z.string().optional(),
        tags: z.array(z.string()).default([]),
        created: z.string().optional(),
        updated: z.string().optional(),
      }),
    }),
  }),
};
