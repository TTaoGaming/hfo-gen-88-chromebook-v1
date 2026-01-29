// Medallion: Bronze | Mutation: 0% | HIVE: V
import { z } from 'zod';

const PortIdSchema = z.enum(['P0', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7']);
const PortLabelSchema = z.enum(['SENSE', 'FUSE', 'SHAPE', 'DELIVER', 'DISRUPT', 'DEFEND', 'STORE', 'NAVIGATE']);

const PowerwordSchema = z.enum([
    'OBSERVE',
    'BRIDGE',
    'SHAPE',
    'INJECT',
    'DISRUPT',
    'IMMUNIZE',
    'ASSIMILATE',
    'NAVIGATE',
]);

const Binary3Schema = z.string().regex(/^[01]{3}$/);

const TrigramSchema = z
    .object({
        name: z.string().min(1),
        symbol: z.string().min(1).optional(),
        element: z.string().min(1),
    })
    .strict();

const FormatsSchema = z
    .object({
        touch2d: z
            .object({
                role: z.literal('cursor_frame'),
                example_fields: z.array(z.string().min(1)).nonempty(),
            })
            .strict()
            .optional(),
        w3c_pointer: z
            .object({
                role: z.literal('platform_event_shape'),
                example_fields: z.array(z.string().min(1)).nonempty(),
            })
            .strict()
            .optional(),
    })
    .strict()
    .optional();

export const HfoLegendaryCommanderInvariantV1Schema = z
    .object({
        port_index: z.number().int().min(0).max(7),
        port_id: PortIdSchema,
        port_label: PortLabelSchema,
        powerword: PowerwordSchema,
        commander_name: z.string().min(1),
        jadc2_domain: z.string().min(1),
        mosaic_tile: z.string().min(1),
        binary: Binary3Schema,
        octree_bits: z.tuple([z.union([z.literal(0), z.literal(1)]), z.union([z.literal(0), z.literal(1)]), z.union([z.literal(0), z.literal(1)])]),
        trigram: TrigramSchema,
        notes: z.array(z.string().min(1)).optional(),
        formats: FormatsSchema,
    })
    .strict()
    .superRefine((v, ctx) => {
        const [b2, b1, b0] = v.octree_bits;
        const expected = `${b2}${b1}${b0}`;
        if (v.binary !== expected) {
            ctx.addIssue({
                code: z.ZodIssueCode.custom,
                message: `binary must match octree_bits (expected ${expected}, got ${v.binary})`,
                path: ['binary'],
            });
        }
    });

export const HfoLegendaryCommandersInvariantsDocV1Schema = z
    .object({
        schema: z.literal('hfo.legendary_commanders.invariants.v1'),
        version: z.literal('v1'),
        created_utc: z.string().min(1),
        locked_fields: z.array(z.string().min(1)).nonempty(),
        holonarchy: z
            .object({
                model: z.literal('fractal_octree'),
                root: z.string().min(1),
                depth_1: z
                    .object({
                        ports: z.literal(8),
                        binary_bits: z.literal(3),
                        address_space: z.array(Binary3Schema).length(8),
                        note: z.string().min(1),
                    })
                    .strict(),
            })
            .strict(),
        ports: z.array(HfoLegendaryCommanderInvariantV1Schema).length(8),
        provenance: z
            .object({
                primary_sources: z.array(z.string().min(1)).nonempty(),
                drift_notes: z.array(z.string().min(1)).optional(),
            })
            .strict(),
    })
    .strict()
    .superRefine((doc, ctx) => {
        const seenPortIndex = new Set<number>();
        const seenPortId = new Set<string>();
        const seenBinary = new Set<string>();

        for (const p of doc.ports) {
            if (seenPortIndex.has(p.port_index)) {
                ctx.addIssue({ code: z.ZodIssueCode.custom, message: `duplicate port_index ${p.port_index}`, path: ['ports'] });
            }
            seenPortIndex.add(p.port_index);

            if (seenPortId.has(p.port_id)) {
                ctx.addIssue({ code: z.ZodIssueCode.custom, message: `duplicate port_id ${p.port_id}`, path: ['ports'] });
            }
            seenPortId.add(p.port_id);

            if (seenBinary.has(p.binary)) {
                ctx.addIssue({ code: z.ZodIssueCode.custom, message: `duplicate binary ${p.binary}`, path: ['ports'] });
            }
            seenBinary.add(p.binary);
        }

        if (seenPortIndex.size !== 8 || seenPortId.size !== 8 || seenBinary.size !== 8) {
            ctx.addIssue({
                code: z.ZodIssueCode.custom,
                message: 'ports must cover 8 unique port_index/port_id/binary values',
                path: ['ports'],
            });
        }
    });
